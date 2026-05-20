import os
import sys
import time
import pickle
from collections import Counter

from embeddings import buildReferenceEmbeddings
from detector import detectGameTopK
from video import videoToFrames, getVideoDetails
from utils import cacheEmbeddings

start = time.time()
if os.path.exists("../cachedEmbeddings/refEmbed.pkl"):
    print("-> Using cached Embedding.\n-> Delete cache if you want to create new embeddings")
        
    with open("../cachedEmbeddings/refEmbed.pkl", "rb") as f:
        referenceEmbeddings = pickle.load(f)

    print("-> Loaded Successfully")
    
else:
    # Build reference embeddings once
    print("-> No cache, building embeddings\n")
    referenceEmbeddings, _ = buildReferenceEmbeddings()
    cacheEmbeddings(referenceEmbeddings)
    print("-> Saved embeddings to cache")

def main():

    print("\n=== AI Game Detector ===")

    inputVideoPath = None

    if len(sys.argv) > 1:
        inputVideoPath = sys.argv[1]

    while True:
        if inputVideoPath is not None: 
            videoPath = inputVideoPath
        else: 
            videoPath = input("Enter video path (or q to quit): ")

        inputVideoPath = None
        if videoPath.lower() == "q":
            break
        
        if not os.path.exists(videoPath):
            print("Video does not exist.\n")
            continue

        clipName = os.path.splitext(
            os.path.basename(videoPath)
        )[0]

        print("\nExtracting frames...")

        if getVideoDetails(videoPath)[2] > 180:
            print("-> Video Length too long, only using the first 3 minutes\n")
            frameFolder = videoToFrames(
                videoPath,
                outputFolder=clipName,
                intervalSeconds=2,
                endTime="03:00"
            )

        else:
            frameFolder = videoToFrames(
                videoPath,
                outputFolder=clipName,
                intervalSeconds=2
            )

        if frameFolder is None:
            print("Frame extraction failed.\n")
            continue

        smallFolder = os.path.join(frameFolder, "small")

        predictions = []
        allTopMatches = []

        for frameFile in os.listdir(smallFolder):

            if not frameFile.endswith(".jpg"):
                continue

            framePath = os.path.join(
                smallFolder,
                frameFile
            )

            result = detectGameTopK(framePath, referenceEmbeddings)
            # print(result, '\n')
            if result["prediction"] == "Unknown Game":
                continue

            predictions.append(result["prediction"])
            allTopMatches.append({
                "frame": framePath,
                "prediction": result["prediction"],
                "confidence": result["confidence"]
            })

        ## Retrevial Level Filter Check
        if len(predictions) == 0:
            print("\nCould not confidently detect game.\n")
            continue

        # Game Confidence (Vote Distribution Normalization)
        gameCounts = Counter(predictions)
        totalCount = len(predictions)
        
        topConfidence = gameCounts.most_common(1)[0][1] / totalCount

        ## Vote Level Filter Check
        if topConfidence < 0.6:
            print("\nCould not confidently determine the game.\n")
            continue

        confidences = {
            game: (count / totalCount) * 100
            for game, count in gameCounts.items()
        }

        sortedConfidences = sorted(
            confidences.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Game Prediction Result
        finalPrediction = gameCounts.most_common(1)[0][0]

        # Best frames from Clip (sorted by confidence)
        sortedFrames = sorted(
            allTopMatches,
            key= lambda x: x["confidence"],
            reverse=True
        )

        topFrames = sortedFrames[:3]

        influentialFrames = [
            item["frame"]
            for item in topFrames
        ]
        
        print(f"\n---> Processing took {time.time() - start:.2f}s <---")

        print(f"\nDetected Game: {finalPrediction}\n")

        print("Confidence Breakdown:\n")
        for k, v in sortedConfidences:
            print(f"{k}: {v:.2f}%")

        print("\nMost Influential Frames from the Clip: ")
        for ref in influentialFrames:
            print(ref)
        
        print("\n---\n")
            

if __name__ == "__main__":
    main()
    # pass