import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	const res = await fetch(`/api/results/${params.id}`);
	const result = await res.json();
	if (result == null) {
		error(404, 'Give id does not exits');
	}
	// console.log(result);
	return result;
};
