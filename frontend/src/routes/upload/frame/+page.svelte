<script lang="ts">
	let frameFile = $state<File | undefined>(undefined);
	let loading = $state(false);
	let errorText = $state<string | undefined>(undefined);
	let result = $state<object | undefined>(undefined);
	const MAX_IMAGE_SIZE = 10 * 1024 * 1024;
	import { API_BASE } from '$lib/config';

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

	async function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		errorText = undefined;
		if (!frameFile) {
			errorText = 'Please select a picture';
			return;
		}
		loading = true;
		try {
			const form = new FormData();
			form.append('file', frameFile);
			const res = await fetch(`${API_BASE}/api/upload/frame`, {
				method: 'POST',
				body: form
			});
			const pred = await res.json();
			// console.log(pred);
			result = {
				prediction: pred['prediction'],
				confidence: pred['confidence']
			};
		} catch (e) {
			console.log(e);
		} finally {
			loading = false;
		}
		// upload
	}
</script>

<section class="container">
	<hgroup>
		<h3>Frame Detection</h3>
		<p>A singular frame is compared against images in the reference library to detect the game.</p>
	</hgroup>
	<span>A picture is required. Supported file formats: .png, .jpg<br /><br />Max size: 10MB</span>
	<div class="container">
		<form onsubmit={handleSubmit} enctype="multipart/form-data">
			<input
				type="file"
				name="framePicker"
				accept=".png,.jpg,.jpeg"
				onchange={handleFrameChange}
				required
				aria-required={true}
				aria-busy={loading}
			/>
			<button type="submit" aria-busy={loading} disabled={loading}>Detect!</button>
		</form>
		{#if errorText}
			<p style:color="red">{errorText}</p>
		{/if}
		{#if result}
			<div class="container">
				<ul>
					<li>Game: {JSON.stringify(result['prediction'])}</li>
					<li>Confidence: {JSON.stringify(result['confidence'])}</li>
				</ul>
			</div>
		{/if}
	</div>
</section>
