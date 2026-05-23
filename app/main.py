import sys
import time

from utils import (
    detectVideo, 
    detectFrame, 
    loadReferenceEmbeddings
)

referenceEmbeddings = loadReferenceEmbeddings()

def main():

    print("\n=== AI Game Detector ===")

    inputPath = None
    startTime = "00:00"
    endTime = None

    if len(sys.argv) > 1:
        inputPath = sys.argv[1]
    if len(sys.argv) > 2:
        startTime = sys.argv[2]
    if len(sys.argv) > 3:
        endTime = sys.argv[3]

    while True:
        if inputPath is not None:
            path = inputPath
        else:
            path = input("Enter video path (or q to quit): ")

        inputPath = None
        if path.lower() == "q":
            break

        start = time.time()
        if path.endswith((".mp4", ".mov", ".avi")):    
            detectVideo(path, referenceEmbeddings=referenceEmbeddings, startTime=startTime, endTime=endTime)

        elif path.endswith((".png", ".jpg", ".jpeg")): 
            detectFrame(path, referenceEmbeddings)

        else:
            
            print("Unsupported File Format")
            print("Only support Video(.mp4, .mov, .avi) and Picture(.png, .jpg, .jpeg)")
        
        print(f"\n---> Processing took {time.time() - start:.2f}s <---")
        print("\n---\n")


if __name__ == "__main__":
    main()
