<script lang="ts">
	let videoFile = $state<File | undefined>(undefined);
	let startTime = $state('00:00');
	let endTime = $state<string | undefined>(undefined);
	let loading = $state(false);
	let errorText = $state<string | undefined>(undefined);
	let re = /^(?:[0-5]\d):(?:[0-5]\d)$/;
	const MAX_VIDEO_SIZE = 500 * 1024 * 1024;

	function handleVideoChange(e: Event) {
		const file = (e.currentTarget as HTMLInputElement).files?.[0];
		errorText = undefined;
		if (!file) return;
		if (file.size > MAX_VIDEO_SIZE) {
			errorText = 'Video must be under 500MB';
			return;
		}
		videoFile = file;
	}

	function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		errorText = undefined;
		if (!videoFile || !startTime) {
			errorText = 'All fields must be filled';
			return;
		}

		if ((startTime && re.test(startTime)) || (endTime && re.test(endTime))) {
			errorText = 'Invalid time format';
			return;
		}

		loading = true;
		console.log('Uploading Video', videoFile, startTime, endTime);
		// upload
		loading = false;
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
		Video file is required. Supported file formats: .mp4, .mov, .avi<br /><br />
		Start Time and End Time are optional. If a length greater than 2 minutes is given it will automatically
		be reduced to a 2 minute limit.
	</span>
	<div class="container">
		<form onsubmit={handleSubmit}>
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
