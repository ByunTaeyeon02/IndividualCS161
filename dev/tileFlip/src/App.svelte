<script>
	import { Route, Router, navigate } from 'svelte-routing';
	import Game from './Game.svelte';
	import Contact from './Contact.svelte';

	export const routes = [
		{ path: '/', component: Contact },
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