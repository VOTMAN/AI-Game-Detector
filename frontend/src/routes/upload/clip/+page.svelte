<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';

	let videoFile = $state<File | undefined>(undefined);
	let startTime = $state('00:00');
	let endTime = $state<string | undefined>(undefined);
	let loading = $state(false);
	let errorText = $state<string | undefined>(undefined);
	let re = /^(?:[0-5]\d):(?:[0-5]\d)$/;
	const MAX_VIDEO_SIZE = 350 * 1024 * 1024;

	function handleVideoChange(e: Event) {
		const file = (e.currentTarget as HTMLInputElement).files?.[0];
		errorText = undefined;
		if (!file) return;
		if (file.size > MAX_VIDEO_SIZE) {
			errorText = 'Video must be under 350MB';
			return;
		}
		videoFile = file;
	}

	async function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		errorText = undefined;
		if (!videoFile) {
			errorText = 'All fields must be filled';
			return;
		}

		if ((startTime && !re.test(startTime)) || (endTime && !re.test(endTime))) {
			errorText = 'Invalid time format';
			return;
		}

		// console.log('Uploading Video', videoFile, startTime, endTime);
		try {
			loading = true;
			const form = new FormData();
			form.append('file', videoFile);
			form.append('startTime', startTime);
			if (endTime) form.append('endTime', endTime);

			const res = await fetch('/api/upload/clip', {
				method: 'POST',
				body: form
			});
			const { id } = await res.json();
			goto(resolve(`/result/${JSON.stringify(id).replaceAll('"', '')}`));
		} catch (e) {
			console.log(e);
		} finally {
			loading = false;
		}
	}
</script>

<section class="container">
	<hgroup>
		<h3>Clip Detection</h3>
		<p>
			The frames from the clip will be extracted (up to 2 mins) and the model will check through its
			reference library and try to detect the game. Only known games are detectable.
		</p>
	</hgroup>
	<span>
		Video file is required. Supported file formats: .mp4, .mov, .avi. Size Limit: 200mb<br /><br />
		Start Time and End Time are optional. If a length greater than 2 minutes is given it will automatically
		be reduced to a 2 minute limit. Ideally server expect a clip of 30 seconds to 1 minute
	</span>
	<div class="container">
		<form onsubmit={handleSubmit} enctype="multipart/form-data">
			<input
				type="file"
				name="videoPicker"
				accept=".mp4,.mov,.avi"
				onchange={handleVideoChange}
				required
				aria-required={true}
			/>
			<label>Start Time: <input type="text" bind:value={startTime} placeholder="MM:SS" /></label>
			<label>End Time: <input type="text" bind:value={endTime} placeholder="MM:SS" /></label>
			<button type="submit" aria-busy={loading} disabled={loading}>Detect!</button>
		</form>
		{#if errorText}
			<p style:color="red">{errorText}</p>
		{/if}
	</div>
</section>
