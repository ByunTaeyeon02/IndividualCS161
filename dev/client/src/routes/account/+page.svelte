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
	let displayedUsername: string;
	let newPassword1: string;
	let newPassword2: string;
	let newUsername: string;

	// alerts
	let successAlert = false;
	let successMsg = "";
	let warningAlert = false;
	let warningMsg = "";

	let isLoggedIn = false;

	let maxChar = 20;

	async function isUserLoggedIn() {
		try {
			const response = await fetch('/protected');
			const data = await response.json();
			console.log(data.loggedIn);
			if (data.loggedIn) {
				getUserInfoFull();
				isLoggedIn = true;
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
			displayedUsername = username;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	onMount(() => {
		displayedUsername = "";
        newPassword1 = "";
		newPassword2 = "";
		newUsername = "";
	});

	function changeUsername() {
		if (newUsername !== "") {
			setUsername(newUsername);
		} else {
			successAlert = false;
			warningAlert = true;
			warningMsg = "Username cannot be blank";
		}
	}

	async function setUsername(username: string) {
		try {
			const response = await fetch('/setUsername', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({username: username})
			});
			const data = await response.json();
			let message = data.message;

			if (message === "User registered successfully") {
				displayedUsername = newUsername;
				newUsername = "";
				successAlert = true;
				warningAlert = false;
				successMsg = "Username changed successfully";
			} else {
				successAlert = false;
				warningAlert = true;
				warningMsg = message;
			}
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	function changePassword() {
		if (newPassword1 === newPassword2 && newPassword1 !== "") {
			setPassword(newPassword1);
		} else if (newPassword1 !== newPassword2) {
			successAlert = false;
			warningAlert = true;
			warningMsg = "Passwords do not match";
		} else {
			successAlert = false;
			warningAlert = true;
			warningMsg = "Password cannot be blank";
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
			successAlert = true;
			warningAlert = false;
			successMsg = "Password changed successfully";
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	$: {
		if (!isLoggedIn) {
			isUserLoggedIn();
		}

		if (successAlert) {
			setTimeout(() => {
				successAlert = false;
			}, 2500);
		}
		if (warningAlert) {
			setTimeout(() => {
				warningAlert = false;
			}, 2500);
		}

		setTimeout(() => {
			console.log("displayedUsername:", displayedUsername);
		}, 2500);

		if (typeof newUsername === 'string') {
			if (newUsername.length > maxChar) {
				newUsername = newUsername.substring(0, maxChar).trim();
			}
		}

		if (typeof newPassword1 === 'string') {
			if (newPassword1.length > maxChar) {
				newPassword1 = newPassword1.substring(0, maxChar).trim();
			}
		}

		if (typeof newPassword2 === 'string') {
			if (newPassword2.length > maxChar) {
				newPassword2 = newPassword2.substring(0, maxChar).trim();
			}
		}
  	} 
</script>

<svelte:head>
	<title>Account</title>
</svelte:head>

<div class="text-column pt-10">
	{#if successAlert}	
		<div role="alert" class="alert">
			<svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
			<span>{successMsg}</span>
		</div>
	{:else if warningAlert}
		<div role="alert" class="alert">
			<svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
			<span>{warningMsg}</span>
		</div>
	{/if}
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
						<td colspan="2">
							<label class="input input-bordered flex items-center gap-2">
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z" /></svg>
								<input type="text" class="grow" placeholder={displayedUsername} bind:value={newUsername}/>
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
	

	.alert {
        position: fixed;
        top: 2vh;
        left: 50%;
        transform: translateX(-50%);
        width: 500px;
        z-index: 1000;
    }
</style>