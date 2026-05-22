<script lang="ts">
	let frameFile = $state<File | undefined>(undefined);
	let loading = $state(false);
	let errorText = $state<string | undefined>(undefined);
	const MAX_IMAGE_SIZE = 10 * 1024 * 1024;

	function handleFrameChange(e: Event) {
		const file = (e.currentTarget as HTMLInputElement).files?.[0];
		errorText = undefined;
		if (!file) return;
		if (file.size > MAX_IMAGE_SIZE) {
			errorText = 'Image must be under 10MB';
			return;
		}
		frameFile = file;
	}

	function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		errorText = undefined;
		if (!frameFile) {
			errorText = 'Please select a picture';
			return;
		}
		loading = true;
		console.log('Uploading Picture', frameFile);
		// upload
		loading = false;
	}
</script>

<section class="container">
	<hgroup>
		<h3>Frame Detection</h3>
		<p>A singular frame is compared against images in the reference library to detect the game.</p>
	</hgroup>
	<span>A picture is required. Supported file formats: .png, .jpg<br /><br />Max size: 10MB</span>
	<div class="container">
		<form onsubmit={handleSubmit}>
			<input
				type="file"
				name="framePicker"
				accept=".png,.jpg,.jpeg"
				onchange={handleFrameChange}
				required
				aria-required={true}
			/>
			<button type="submit" aria-busy={loading} disabled={loading}>Detect!</button>
		</form>
		{#if errorText}
			<p style:color="red">{errorText}</p>
		{/if}
	</div>
</section>
