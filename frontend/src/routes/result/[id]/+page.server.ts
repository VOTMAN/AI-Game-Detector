import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { DetectionResult } from '$lib/types';
import { API_BASE } from '$lib/config';

export const load: PageServerLoad = async ({ fetch, params }) => {
	while (true) {
		const res = await fetch(`${API_BASE}/api/results/${params.id}`);

		if (!res.ok) {
			error(404, 'Given id does not exist');
		}

		const result: DetectionResult = await res.json();

		if (result.status === 'done' || result.status === 'failed') {
			return result;
		}

		await new Promise((r) => setTimeout(r, 3000));
	}
};
