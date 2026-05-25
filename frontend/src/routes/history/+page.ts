import type { PageLoad } from './$types';
import type { DetectionResult } from '$lib/types';
import { API_BASE } from '$lib/config';

export const load: PageLoad = async ({ fetch }) => {
	const res = await fetch(`${API_BASE}/api/results/all`);
	const result: DetectionResult[] = await res.json();
	console.log(result);
	if (result.length <= 0) {
		return {
			error: 'No predictions to show'
		};
	}
	return { result };
};
