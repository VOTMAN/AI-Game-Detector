import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { DetectionResult } from '$lib/types';
import { API_BASE } from '$lib/config';

export const load: PageServerLoad = async ({ fetch, params }) => {
	const res = await fetch(`${API_BASE}/api/results/${params.id}`);
	const result: DetectionResult = await res.json();
	if (result == null) {
		error(404, 'Give id does not exits');
	}
	// console.log(result);
	return result;
};
