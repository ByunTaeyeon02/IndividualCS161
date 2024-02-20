<script>
	import { Route, Router, navigate } from 'svelte-routing';
	import './styles/main.css';
	import Game from './Game.svelte';

	export const routes = [
		{ path: '/', component: Game },
		{ path: '/game', component: Game },
	];
</script>

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