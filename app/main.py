import os
import pickle
import sys
import time
from collections import Counter

from detector import detectGameTopK
from embeddings import buildReferenceEmbeddings
from utils import cacheEmbeddings
from video import getVideoDetails, videoToFrames

if os.path.exists("../cachedEmbeddings/refEmbed.pkl"):
    print(
        "-> Using cached Embedding.\n-> Delete cache if you want to create new embeddings"
    )

    with open("../cachedEmbeddings/refEmbed.pkl", "rb") as f:
        referenceEmbeddings = pickle.load(f)

    print("-> Loaded Successfully")

else:
    # Build reference embeddings once
    print("-> No cache, building embeddings\n")
    referenceEmbeddings, _ = buildReferenceEmbeddings()
    cacheEmbeddings(referenceEmbeddings)
    print("-> Saved embeddings to cache")

def detectVideo(path):
    print("VIDEO DETECTION: ")
    if not os.path.exists(path):
        print("Video does not exist.\n")
        return

    clipName = os.path.splitext(os.path.basename(path))[0]

    print("\nExtracting frames...")

    if getVideoDetails(path)[2] > 180:
        print("-> Video Length too long, only using the first 3 minutes\n")
        frameFolder = videoToFrames(
            path, outputFolder=clipName, intervalSeconds=2, endTime="03:00"
        )

    else:
        frameFolder = videoToFrames(
            path, outputFolder=clipName, intervalSeconds=2
        )

    if frameFolder is None:
        print("Frame extraction failed.\n")
        return

    smallFolder = os.path.join(frameFolder, "small")

    predictions = []
    allTopMatches = []

    for frameFile in os.listdir(smallFolder):
        if not frameFile.endswith(".jpg"):
            continue

        framePath = os.path.join(smallFolder, frameFile)

        result = detectGameTopK(framePath, referenceEmbeddings)
        # print(result, '\n')
        if result["prediction"] == "Unknown Game":
            continue

        predictions.append(result["prediction"])
        allTopMatches.append(
            {
                "frame": framePath,
                "prediction": result["prediction"],
                "confidence": result["confidence"],
            }
        )

    ## Retrevial Level Filter Check
    if len(predictions) == 0:
        print("\nCould not confidently detect game.\n")
        return

    # Game Confidence (Vote Distribution Normalization)
    gameCounts = Counter(predictions)
    totalCount = len(predictions)

    topConfidence = gameCounts.most_common(1)[0][1] / totalCount

    ## Vote Level Filter Check
    if topConfidence < 0.6:
        print("\nCould not confidently determine the game.\n")
        return

    confidences = {
        game: (count / totalCount) * 100 for game, count in gameCounts.items()
    }

    sortedConfidences = sorted(
        confidences.items(), key=lambda x: x[1], reverse=True
    )

    # Game Prediction Result
    finalPrediction = gameCounts.most_common(1)[0][0]

    # Best frames from Clip (sorted by confidence)
    sortedFrames = sorted(
        allTopMatches, key=lambda x: x["confidence"], reverse=True
    )

    topFrames = sortedFrames[:3]

    influentialFrames = [item["frame"] for item in topFrames]


    print(f"\nDetected Game: {finalPrediction}\n")

    print("Confidence Breakdown:\n")
    for k, v in sortedConfidences:
        print(f"{k}: {v:.2f}%")

    print("\nMost Influential Frames from the Clip: ")
    for ref in influentialFrames:
        print(ref)

    return finalPrediction, sortedConfidences, influentialFrames

def detectFrame(path):
    if not os.path.exists(path):
        print("Image does not exist.\n")
        return
    result = detectGameTopK(path, referenceEmbeddings)
    print("IMAGE DETECTION:\n")
    print("\nGame: ", result["prediction"])
    if result["prediction"] != "Unknown Game":
        print("Confidence:  ", result["confidence"])

    return result["prediction"], result["confidence"] 

def main():

    print("\n=== AI Game Detector ===")

    inputPath = None

    if len(sys.argv) > 1:
        inputPath = sys.argv[1]

    while True:
        if inputPath is not None:
            path = inputPath
        else:
            path = input("Enter video path (or q to quit): ")

        inputPath = None
        if path.lower() == "q":
            break

        start = time.time()
        if path.endswith((".mp4", ".mpv", ".avi")):
            detectVideo(path)
        elif path.endswith((".png", ".jpg", ".jpeg")): 
            detectFrame(path)
        else:
            print("Unsupported File Format")
            print("Only support Video(.mp4, .mov, .avi) and Picture(.png, .jpg, .jpeg)")
        print(f"\n---> Processing took {time.time() - start:.2f}s <---")
        print("\n---\n")


if __name__ == "__main__":
    main()
    # pass
