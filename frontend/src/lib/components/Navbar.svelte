<script>
	import { resolve } from '$app/paths';
	import ThemeToggle from './ThemeToggle.svelte';

	function toggleTheme() {
		const html = document.documentElement;
		const next = html.dataset.theme === 'light' ? 'dark' : 'light';
		html.dataset.theme = next;
		localStorage.setItem('theme', next);
	}
</script>

<nav class="container">
	<span>AI Game Detector</span>
	<ul>
		<li><a href={resolve('/')}>Home</a></li>
		<li><a href={resolve('/upload/frame')}>Upload Frame</a></li>
		<li><a href={resolve('/upload/clip')}>Upload Clip</a></li>
		<li><a href={resolve('/history')}>History</a></li>
		<li><ThemeToggle onclick={toggleTheme} /></li>
	</ul>
</nav>

<style>
	nav {
		display: flex;
		align-items: center;
	}
</style>
