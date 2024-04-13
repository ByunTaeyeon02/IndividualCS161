<script lang="ts">
	// TODO: finished change Username and Password

	import { onMount } from 'svelte';
	
	// fetched data
	let username: string;
	let userType: string;
	let puzzleCompleted: number;
	let numOfHints: number;
	let numOfHintsUsed: number;
	let numOfGiveUpsUsed: number;

	// inputs
	let newPassword1: string;
	let newPassword2: string;
	let newUsername: string;

	async function isUserLoggedIn() {
		try {
			const response = await fetch('/protected');
			const data = await response.json();
			console.log(data.loggedIn);
			if (data.loggedIn) {
				getUserInfoFull();
			} else {
				window.location.href = '/';
			}
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function getUserInfoFull() { 
		try {
			const response = await fetch('/getUserInfo');
			const data = await response.json();
			username = data.username;
			userType = data.userType;
			puzzleCompleted = data.puzzleCompleted;
			numOfHints = data.numOfHints;
			numOfHintsUsed = data.numOfHintsUsed;
			numOfGiveUpsUsed = data.numOfGiveUpsUsed;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	onMount(() => {
        isUserLoggedIn();
		newPassword1 = "";
		newPassword2 = "";
		newUsername = "";
	});

	function changeUsername() {
		if (newUsername !== "") {
			console.log(newUsername);
			username = newUsername;
			setUsername(newUsername);
		}
	}

	async function setUsername(username: string) {
		try {
			const response = await fetch('/setUsername', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({username: username})
			});
			username = "";
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	function changePassword() {
		if (newPassword1 === newPassword2 && newPassword1 !== "") {
			console.log(newPassword1);
			setPassword(newPassword1);
		}
	}

	async function setPassword(password: string) {
		try {
			const response = await fetch('/setPassword', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({password: password})
			});
			newPassword1 = "";
			newPassword2 = "";
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}
</script>

<svelte:head>
	<title>Account</title>
</svelte:head>

<div class="text-column pt-10">
	<div class="pb-6">
		<h1>Account Settings</h1>
	</div>
	<div class="card w-300 shadow-xl pl-5 pb-4 rounded-3xl">
		<div class="overflow-x-auto">
			<table class="table">
				<tbody>
					<tr class="hover"> 
						<th>Account Type</th>
						<td>{userType}</td>
					</tr>
					<tr class="hover"> 
						<th>Username</th>
						<td>{username}</td>
						<td>
							<label class="input input-bordered flex items-center gap-2">
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z" /></svg>
								<input type="text" class="grow" placeholder="New username" bind:value={newUsername}/>
							 </label>
						</td>
						<td>
							<button class="btn btn-outline shadow-xl" on:click={changeUsername}>Confirm</button>
						</td>
					</tr>
					<tr class="hover"> 
						<th>Password</th>
						<td>
							<label class="input input-bordered flex items-center gap-2">
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path fill-rule="evenodd" d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z" clip-rule="evenodd" /></svg>
								<input type="password" class="grow" placeholder="New password" bind:value={newPassword1}/>
							</label>
						</td>
						<td>
							<label class="input input-bordered flex items-center gap-2">
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path fill-rule="evenodd" d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z" clip-rule="evenodd" /></svg>
								<input type="password" class="grow" placeholder="Re-enter password" bind:value={newPassword2}/>
							</label>
						</td>
						<td>
							<button class="btn btn-outline shadow-xl" on:click={changePassword}>Confirm</button>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
	
	<div class="pt-20 pb-4">
		<h1>Account Stats</h1>
	</div>
	<div class="card w-300 shadow-xl pl-5 pb-4 rounded-3xl">
		<div class="overflow-x-auto">
			<table class="table">
				<thead>
					<tr>
						<th></th>
						<th>Completed</th>
						<th>Give ups</th>
						<th>Total</th>
					</tr>
				  </thead>
				<tbody>
					<tr class="hover"> 
						<th>Puzzles</th>
						<td>{puzzleCompleted}</td>
						<td>{numOfGiveUpsUsed}</td>
						<td>{puzzleCompleted + numOfGiveUpsUsed}</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
	<div class="pb-10"></div>
	<div class="card w-300 shadow-xl pl-5 pb-4 rounded-3xl">
		<div class="overflow-x-auto">
			<table class="table">
				<thead>
					<tr>
						<th></th>
						<th>Current</th>
						<th>Used</th>
						<th>Total</th>
					</tr>
				  </thead>
				<tbody>
					<tr class="hover"> 
						<th>Hints</th>
						<td>{numOfHints}</td>
						<td>{numOfHintsUsed}</td>
						<td>{numOfHints + numOfHintsUsed}</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</div>


<style>
	button,input,h1,tr,td {
		font-family: 'BadComic';
	}
</style>