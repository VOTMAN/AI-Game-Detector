<script lang="ts">
	import type { PageProps } from './$types';
	import { resolve } from '$app/paths';

	let images: string[] = $state([]);
	let errorText: string | null = $state(null);
	let { data }: PageProps = $props();

	async function getImages() {
		const id = data.id;
		const paths = data.frames;
		for (const path of paths!) {
			const filename = path.split('/')[4];
			const res = await fetch(`/api/frames/${id}/${filename}`);
			const img = await res.blob();
			console.log(img);
			if (img.type == 'application/json') {
				errorText = 'No Images, Images cleared from server. ';
				return;
			}
			const imgUrl = URL.createObjectURL(img);
			images = [...images, imgUrl];
		}
		console.log(images);
	}
</script>

<div class="container">
	<a href={resolve('/history')} class="secondary back-link">
		<i class="ti ti-arrow-left" aria-hidden="true"></i> back to history
	</a>

	<div class="clip-header">
		<h1>{data.clip_name}</h1>
		<p class="muted">Uploaded at: {new Date(data.created_datetime).toLocaleString()}</p>
	</div>

	<div class="meta-cards">
		<div class="meta-card">
			<p class="label">Prediction</p>
			<p class="value">{data.prediction}</p>
		</div>
		<div class="meta-card">
			<p class="label">Top confidence</p>
			<p class="value">{data.confidences[0][1].toFixed(1)}%</p>
		</div>
		<div class="meta-card">
			<p class="label">Time taken</p>
			<p class="value">{data.time_taken.toFixed(2)}s</p>
		</div>
	</div>

	<article>
		<p class="section-label">Confidence breakdown</p>
		<div class="breakdown">
			{#each data.confidences as game (game[0])}
				<div class="bar-row">
					<div class="bar-meta">
						<span>{game[0]}</span>
						<span class="bar-pct">{game[1].toFixed(1)}%</span>
					</div>
					<progress value={game[1]} max="100"></progress>
				</div>
			{/each}
		</div>
	</article>

	<article>
		<p class="section-label">Most influential frames</p>
		{#if images.length > 0}
			<div class="frames-grid">
				{#each images as img (img)}
					<img src={img} alt="Influential frame" />
				{/each}
			</div>
		{:else}
			<div class="frames-placeholder">
				{#each [0, 1, 2] as i (i)}
					<div class="frame-empty">
						<i class="ti ti-photo" aria-hidden="true"></i>
					</div>
				{/each}
			</div>
			<button class="outline secondary load-btn" onclick={getImages}>
				<i class="ti ti-photo-down" aria-hidden="true"></i> Load images
			</button>
		{/if}
		{#if errorText}
			<p class="error-text">{errorText}</p>
		{/if}
	</article>
</div>

<style>
	.back-link {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		font-size: 13px;
		text-decoration: none;
		margin-bottom: 1.5rem;
	}

	.clip-header {
		margin-bottom: 1.5rem;
	}

	.clip-header h1 {
		margin: 0 0 4px;
	}

	.muted {
		font-size: 13px;
		color: var(--pico-muted-color);
		margin: 0;
	}

	.meta-cards {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
		gap: 12px;
		margin-bottom: 1.5rem;
	}

	.meta-card {
		background: var(--pico-card-sectioning-background-color);
		border-radius: var(--pico-border-radius);
		padding: 1rem;
	}

	.label {
		font-size: 13px;
		color: var(--pico-muted-color);
		margin: 0 0 4px;
	}

	.value {
		font-size: 20px;
		font-weight: 500;
		margin: 0;
		color: var(--pico-color);
	}

	.section-label {
		font-size: 13px;
		color: var(--pico-muted-color);
		font-weight: 500;
		margin: 0 0 12px;
	}

	.breakdown {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.bar-row {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.bar-meta {
		display: flex;
		justify-content: space-between;
		font-size: 13px;
	}

	.bar-pct {
		font-weight: 500;
	}

	.breakdown progress {
		width: 100%;
		height: 8px;
		margin: 0;
	}

	.frames-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 8px;
	}

	.frames-grid img {
		width: 100%;
		aspect-ratio: 16 / 9;
		object-fit: cover;
		border-radius: var(--pico-border-radius);
	}

	.frames-placeholder {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 8px;
		margin-bottom: 12px;
	}

	.frame-empty {
		aspect-ratio: 16 / 9;
		background: var(--pico-card-sectioning-background-color);
		border-radius: var(--pico-border-radius);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 24px;
		color: var(--pico-muted-color);
	}

	.load-btn {
		width: 100%;
		margin-top: 4px;
	}

	.error-text {
		font-size: 13px;
		color: var(--pico-del-color);
		margin: 8px 0 0;
	}
</style>
