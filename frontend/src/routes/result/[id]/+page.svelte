<script lang="ts">
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<section class="container">
	{JSON.stringify(data)}
</section>
