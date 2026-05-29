<script lang="ts">
	import type { PageProps } from './$types';
	import { resolve } from '$app/paths';
	import { API_BASE } from '$lib/config';

	const { data }: PageProps = $props();
	const predList = data.result;

	let searchQuery: string = $state('');
	let searchResults: string[] | null = $state(null); // null = no search, [] = no results
	let searching: boolean = $state(false);
	let timeout: ReturnType<typeof setTimeout>;

	async function searchClips(query: string) {
		searching = true;
		console.log('Searching: ', query);
		const res = await fetch(`${API_BASE}/api/search/${query}`);
		const result = await res.json();

		const ids = result[0]?.map((m: any) => m.id) ?? [];
		searchResults = ids;
		searching = false;
	}

	$effect(() => {
		clearTimeout(timeout);

		if (!searchQuery.trim()) {
			searchResults = null; // reset to show all
			return;
		}

		timeout = setTimeout(() => {
			searchClips(searchQuery);
		}, 1000);

		return () => clearTimeout(timeout);
	});
</script>

<header class="container">
	<hgroup>
		<article>
			<div>
				<h3>Prediction History</h3>
				<p>
					Semantic Search using chromaDB, try giving a query like 'Elden Ring Messmer' or 'Valorant
					Ace' to get approximate results
				</p>
			</div>
			<br />
			<input
				type="text"
				bind:value={searchQuery}
				placeholder="Search Clips"
				aria-busy={searching}
			/>
		</article>
		<p>
			View all previously processed clips and their detection results. Currently shared globally for
			all users.
		</p>
	</hgroup>
</header>
<section class="container">
	{#if data.error || !predList || predList.length === 0}
		<article class="empty-state">
			<i class="ti ti-history-off" aria-hidden="true"></i>
			<p>No predictions yet. Upload a Clip to get started.</p>
			<div class="empty-actions">
				<a href={resolve('/upload/clip')} role="button">Upload clip</a>
			</div>
		</article>
	{:else}
		{@const displayList =
			searchResults !== null
				? predList
						.filter((r) => searchResults!.includes(r.id))
						.sort((a, b) => searchResults!.indexOf(a.id) - searchResults!.indexOf(b.id))
				: predList.filter((r) => r.status === 'done' || r.status === 'processing')}

		{#if searching}
			<progress></progress>
		{:else if displayList.length === 0 && searchQuery.trim()}
			<article style="text-align: center; padding: 2rem;">
				<p style="color: var(--pico-muted-color);">No clips found for "{searchQuery}"</p>
			</article>
		{:else}
			<div class="history-list">
				{#each displayList as result (result.id)}
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
								<span class="prediction-badge">
									{result.status === 'processing'
										? 'Processing...'
										: result.status === 'failed'
											? 'Failed'
											: result.prediction}
								</span>
								{#if result.confidences && result.confidences.length > 0}
									<span class="confidence-text"
										>{result.confidences[0][1].toFixed(2)}% confidence</span
									>
								{/if}
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
	{/if}
</section>

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
