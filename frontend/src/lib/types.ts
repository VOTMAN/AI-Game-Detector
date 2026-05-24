type DetectionResult = {
    id: string,
    clip_name: string,
    prediction: string,
    confidence: Array<string | number>[] | null,
    frames: Array<string> | null,
    time_taken: number
    created_at: Date
}