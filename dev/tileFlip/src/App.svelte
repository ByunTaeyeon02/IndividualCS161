<script lang="ts">
	import { Router, Route, Link, navigate } from 'svelte-routing';
 	import Home from './Home.svelte';
  	import Projects from './Projects.svelte';
  	import Contact from './Contact.svelte';
	import Navbar from './components/Navbar.svelte';

	let message = '';

	async function fetchData() {
		try {
		const response = await fetch('http://localhost:5000/');
		const data = await response.json();
		message = data.message;
		} catch (error) {
		console.error('Error fetching data:', error);
		message = 'Error fetching data from the backend';
		}
	}
	fetchData();

	const routes = [
		{ path: "/", component: Home },
		{ path: "/Projects", component: Projects },
		{ path: "/Contact", component: Contact },
	];

	export let url = "";
	let currentUrl = window.location.pathname;
</script>

<html lang="en">
	<main>
		<Navbar/>
		<h1>{message}</h1>
		<Router {url}>
			<div>
			  {#each routes as route}
				<Route path={route.path} component={route.component} />
			  {/each}
			</div>
		</Router>
	</main>
</html>

<style>
	@import '/styles/base.css';
	@import '/styles/components.css';
	@import '/styles/utilities.css'; 
</style>