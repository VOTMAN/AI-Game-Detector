import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
// import type { DetectionResult } from '$lib/types';
import { API_BASE } from '$lib/config';
export const prerender = false;

export const load: PageServerLoad = async ({ fetch, params }) => {
	while (true) {
		const res = await fetch(`${API_BASE}/api/results/${params.id}`);

		if (!res.ok) {
			error(404, 'Given id does not exist');
		}

		return await res.json();
	}
};
