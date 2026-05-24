type DetectionResult = {
    id: string,
    prediction: string,
    confidence: Array<string | number>[] | null,
    frames: Array<string> | null,
    time_taken: number
}