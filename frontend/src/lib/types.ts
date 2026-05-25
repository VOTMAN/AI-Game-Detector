export type DetectionResult = {
	id: string;
	status: 'processing' | 'done' | 'failed';
	clip_name: string;
	prediction: string;
	confidences: [string, number][] | null;
	frames: string[] | null;
	time_taken: number;
	created_datetime: Date;
};
