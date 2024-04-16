<script lang="ts">
	import Header from './Header.svelte';
	import './styles.css';

	/*
	import { Router, Link, Route } from "svelte-routing";
  	import Game from "./+page.svelte";
  	import Account from "./account/+page.svelte";
	import Score from "./score/+page.svelte";

	const routes = [
		{ path: "/", component: Game },
		{ path: "/account", component: Account },
		{ path: "/score", component: Score },
	];

	export let url = "";
  	let currentUrl = window.location.pathname; */
</script>

<div class="app">
	<Header />

	<main>
		<slot />
	</main>

	<footer class="footer p-4">
		<nav class="grid-flow-col gap-4 md:place-self-center md:justify-self-end">
			<p>Copyright © 2024 - All right reserved</p>
		</nav>
	</footer>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 85rem;
		margin: 0 auto;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>
