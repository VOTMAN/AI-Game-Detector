<script lang="ts">
	import type { PageProps } from './$types';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { API_BASE } from '$lib/config';

	let layoutOption: boolean = $state(false);
	const { data }: PageProps = $props();

	const predList = data.result;
</script>

<header class="container">
	<hgroup>
		<article>
			<div class="grid">
				<h3>Prediction History</h3>
				<button onclick={() => (layoutOption = !layoutOption)} class="contrast"
					>Change layout</button
				>
			</div>
		</article>
		<p>
			View all previously processed clips and their detection results. Currently shared globally for
			all users.
		</p>
	</hgroup>
</header>
<section class="container">
	{#if !layoutOption}
		{#if data.error || !predList || predList.length === 0}
			<article class="empty-state">
				<i class="ti ti-history-off" aria-hidden="true"></i>
				<p>No predictions yet. Upload a Clip to get started.</p>
				<div class="empty-actions">
					<a href={resolve('/upload/clip')} role="button">Upload clip</a>
				</div>
			</article>
		{:else}
			<div class="history-list">
				{#each predList as result (result.id)}
					<article class="history-card">
						<div class="card-main">
							<div class="card-info">
								<p class="clip-name">{result.clip_name}</p>
								<p class="card-meta">
									<i class="ti ti-clock" aria-hidden="true"></i>
									{new Date(result.created_datetime).toLocaleString()}
									<span class="dot">·</span>
									<i class="ti ti-timer" aria-hidden="true"></i>
									{result.time_taken.toFixed(2)}s
								</p>
							</div>
							<div class="card-right">
								<span class="prediction-badge">{result.prediction}</span>
								<span class="confidence-text"
									>{result.confidences![0][1].toFixed(2)}% confidence</span
								>
							</div>
						</div>
						<footer class="card-footer">
							<a
								href={resolve(`/result/${result.id}`)}
								role="button"
								class="outline secondary view-btn"
							>
								<i class="ti ti-eye" aria-hidden="true"></i> View results
							</a>
						</footer>
					</article>
				{/each}
			</div>
		{/if}

		<style>
			hgroup {
				margin-bottom: 1.5rem;
			}

			hgroup p {
				color: var(--pico-muted-color);
				margin: 0;
			}

			.empty-state {
				display: flex;
				flex-direction: column;
				align-items: center;
				justify-content: center;
				gap: 1rem;
				padding: 3rem 1rem;
				text-align: center;
				color: var(--pico-muted-color);
			}

			.empty-state i {
				font-size: 48px;
			}

			.empty-state p {
				margin: 0;
				font-size: 15px;
			}

			.empty-actions {
				display: flex;
				gap: 12px;
			}

			.history-list {
				display: flex;
				flex-direction: column;
				gap: 12px;
			}

			.history-card {
				margin: 0;
				padding: 1rem 1.25rem;
			}

			.card-main {
				display: flex;
				align-items: flex-start;
				justify-content: space-between;
				gap: 1rem;
			}

			.card-info {
				display: flex;
				flex-direction: column;
				gap: 4px;
				min-width: 0;
			}

			.clip-name {
				font-weight: 500;
				margin: 0;
				font-size: 15px;
				white-space: nowrap;
				overflow: hidden;
				text-overflow: ellipsis;
			}

			.card-meta {
				font-size: 12px;
				color: var(--pico-muted-color);
				margin: 0;
				display: flex;
				align-items: center;
				gap: 4px;
			}

			.card-meta i {
				font-size: 13px;
			}

			.dot {
				opacity: 0.4;
			}

			.card-right {
				display: flex;
				flex-direction: column;
				align-items: flex-end;
				gap: 4px;
				flex-shrink: 0;
			}

			.prediction-badge {
				font-size: 12px;
				font-weight: 500;
				padding: 3px 10px;
				border-radius: 999px;
				background: var(--pico-primary-background);
				color: var(--pico-primary-inverse);
				white-space: nowrap;
			}

			.confidence-text {
				font-size: 12px;
				color: var(--pico-muted-color);
			}

			.card-footer {
				margin-top: 12px;
				padding-top: 12px;
				border-top: 1px solid var(--pico-muted-border-color);
			}

			.view-btn {
				font-size: 13px;
				padding: 6px 14px;
			}
		</style>
	{:else}
		{#if !data.error && predList!.length > 0}
			<div class="grid">
				{#each predList as result (result.id)}
					<article class="prediction-card">
						<header>
							<strong>{result.prediction}</strong>
						</header>

						<img
							src={`${API_BASE}${result.frames![0]}`}
							alt={result.prediction}
							class="preview-image"
						/>

						<h5>{result.clip_name}</h5>

						<p>
							<b>Detected Game:</b>
							{result.prediction}
						</p>

						<p>
							<b>Top Confidence:</b>
							{result.confidences![0][1].toFixed(2)}%
						</p>

						<p>
							<b>Processing Time:</b>
							{result.time_taken.toFixed(2)}s
						</p>

						<small>
							{new Date(result.created_datetime).toLocaleString()}
						</small>

						<footer>
							<button class="secondary" onclick={() => goto(resolve(`/result/${result.id}`))}>
								View Result
							</button>
						</footer>
					</article>
				{/each}
			</div>
		{:else}
			<article>
				<h5>No prediction history available</h5>
				<p>Upload a clip to start generating results.</p>
			</article>
		{/if}

		<style>
			.prediction-card {
				display: flex;
				flex-direction: column;
				gap: 0.75rem;
			}

			.preview-image {
				width: 100%;
				height: 220px;
				object-fit: cover;
				border-radius: 0.75rem;
			}

			footer {
				margin-top: auto;
			}
		</style>
	{/if}
</section>
