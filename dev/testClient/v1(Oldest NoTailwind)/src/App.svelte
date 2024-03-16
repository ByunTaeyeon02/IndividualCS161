<script lang="js">
	import { Route, Router, navigate } from 'svelte-routing';
	import Game from './Game.svelte';
	import Score from './Score.svelte';
	import Settings from './Settings.svelte';
	import TailwindCss from './lib/TailwindCSS.svelte';

	export const routes = [
		{ path: "/", component: Game },
		{ path: "/Score", component: Score },
		{ path: "/Settings", component: Settings },
	];
</script>

<TailwindCss />

<html lang="en">
	<body>
		<main>
			<Router>
				{#each routes as route}
					<Route path={route.path} component={route.component} />
				{/each}
			</Router>
		</main>
	</body>
</html>