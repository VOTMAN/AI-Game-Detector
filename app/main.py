import os
import pickle
from collections import Counter

from embeddings import buildReferenceEmbeddings
from detector import detectGameTopK
from video import videoToFrames, getVideoDetails
from utils import cacheEmbeddings

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

    print("\n=== AI Game Detector ===\n")

    while True:

        videoPath = input("Enter video path (or q to quit): ")

        if videoPath.lower() == "q":
            break

        if not os.path.exists(videoPath):
            print("Video does not exist.\n")
            continue

        clipName = os.path.splitext(
            os.path.basename(videoPath)
        )[0]

        print("\nExtracting frames...")

        if getVideoDetails(videoPath)[2] > 120:
            print("-> Video Length too long, only using the first 2 minutes\n")
            frameFolder = videoToFrames(
                videoPath,
                outputFolder=clipName,
                intervalSeconds=2,
                endTime="02:00"
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

        for frameFile in os.listdir(smallFolder):

            if not frameFile.endswith(".jpg"):
                continue

            framePath = os.path.join(
                smallFolder,
                frameFile
            )

            result = detectGameTopK(framePath, referenceEmbeddings)

            if result == "Unknown Game":
                continue

            predictions.append(result["prediction"])

        if len(predictions) == 0:
            print("\nCould not confidently detect game.\n")
            continue

        finalPrediction = Counter(
            predictions
        ).most_common(1)[0][0]

        print(f"\nDetected Game: {finalPrediction}\n")
        # print(f"Detector Result: {result}\n")


if __name__ == "__main__":
    main()
    # pass