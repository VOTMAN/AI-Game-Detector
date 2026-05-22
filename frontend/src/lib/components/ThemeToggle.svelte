<script lang="ts">
	import type { HTMLButtonAttributes } from 'svelte/elements';

	interface Props extends Omit<HTMLButtonAttributes, 'children' | 'title'> {
		duration?: number;
		ariaLabel?: string;
		class?: string;
		title?: string;
	}

	let {
		duration = 700,
		type = 'button' as HTMLButtonAttributes['type'],
		title = 'Toggle theme',
		ariaLabel = 'Toggle theme',
		class: className = 'themeToggleBtn',
		...restProps
	}: Props = $props();
</script>

<button {type} {title} aria-label={ariaLabel} class={className} {...restProps}>
	<svg
		width="1.2em"
		height="1.2em"
		viewBox="0 0 32 32"
		aria-hidden="true"
		stroke-width="2"
		stroke="currentColor"
		fill="currentColor"
		stroke-linecap="round"
		style="--dur: {duration}ms"
	>
		<path
			stroke-width="1"
			d="M9.4 9.9c1.8-1.8 4.1-2.7 6.6-2.7 5.1 0 9.3 4.2 9.3 9.3 0 2.3-.8 4.4-2.3 6.1-.7.8-2 2.8-2.5 4.4 0 .2-.2.4-.5.4-.2 0-.4-.2-.4-.5v-.1c.5-1.8 2-3.9 2.7-4.8 1.4-1.5 2.1-3.5 2.1-5.6 0-4.7-3.7-8.5-8.4-8.5-2.3 0-4.4.9-5.9 2.5-1.6 1.6-2.5 3.7-2.5 6 0 2.1.7 4 2.1 5.6.8.9 2.2 2.9 2.7 4.9 0 .2-.1.5-.4.5h-.1c-.2 0-.4-.1-.4-.4-.5-1.7-1.8-3.7-2.5-4.5-1.5-1.7-2.3-3.9-2.3-6.1 0-2.3 1-4.7 2.7-6.5z"
		/>
		<path d="M19.8 27.5h-7.6" />
		<path d="M19.8 29.2h-7.6" />
		<path d="M19.8 30.9h-7.6" />
		<path
			pathLength="1"
			fill="none"
			d="M14.6 27.1c0-3.4 0-6.8-.1-10.2-.2-1-1.1-1.7-2-1.7-1.2-.1-2.3 1-2.2 2.3.1 1 .9 1.9 2.1 2h7.2c1.1-.1 2-1 2.1-2 .1-1.2-1-2.3-2.2-2.3-.9 0-1.7.7-2 1.7 0 3.4 0 6.8-.1 10.2"
			class="ray"
		/>
		<path d="M16 5V1.3" pathLength="1" stroke-width="1.5" class="ray" />
		<path d="M27.5 15.8h3.9" pathLength="1" stroke-width="1.5" class="ray" />
		<path d="M23.6 7.9 26.3 5.4" pathLength="1" stroke-width="1.5" class="ray" />
		<path d="M8.4 7.9 5.7 5.4" pathLength="1" stroke-width="1.5" class="ray" />
		<path d="M4.5 15.8H.6" pathLength="1" stroke-width="1.5" class="ray" />
	</svg>
</button>

<style>
	.themeToggleBtn {
		all: unset;
		background: none;
		outline: none;
		border: none;
		cursor: pointer;
		/*filter: drop-shadow(0 0 10px black) drop-shadow(0 0 12px black);*/
	}

	.themeToggleBtn:focus {
		all: unset;
		border: none;
		outline: none;
	}
	.ray {
		stroke-dasharray: 1.1;
		stroke-dashoffset: 0;
		opacity: 1;
		transition:
			stroke-dashoffset var(--dur, 500ms) ease,
			opacity var(--dur, 500ms) ease;
	}

	:global([data-theme='dark']) .themeToggleBtn {
		color: white;
		filter: drop-shadow(0 0 1px white) drop-shadow(0 0 8px white) drop-shadow(0 0 10px white)
			drop-shadow(0 0 18px white);
	}
	:global([data-theme='dark']) .ray {
		stroke-dashoffset: 1;
		opacity: 0;
	}
</style>
