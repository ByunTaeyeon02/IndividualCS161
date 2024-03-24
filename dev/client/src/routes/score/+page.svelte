<script lang="ts">
	import { onMount } from 'svelte';
	
	// fetched data
	let username: string;
	let userType: string;
	let puzzleCompleted: number;
	let numOfHints: number;
	let numOfHintsUsed: number;
	let numOfGiveUpsUsed: number;

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
	});
</script>

<svelte:head>
	<title>Score</title>
</svelte:head>

<div class="text-column">
	<div>
		<h2>Your Score</h2>
		<table style="width: 80vw;">
			<tr>
				<td>
					<div class="stat card shadow-xl rounded-3xl statDisplay">
						<div class="stat-figure text-secondary">
							<div class="radial-progress" style="--value:70;" role="progressbar">{puzzleCompleted / (numOfGiveUpsUsed + puzzleCompleted)}</div>
						</div>
						<div class="stat-title">Puzzles Completed</div>
						<div class="stat-value">{puzzleCompleted}</div>
						<div class="stat-desc">Puzzles completed without giving up</div>
					</div>
				</td>
				<td>
					<div class="stat card shadow-xl rounded-3xl statDisplay">
						<div class="stat-figure text-secondary">
							<div class="radial-progress" style="--value:70;" role="progressbar">{numOfHints / (numOfHints + numOfHintsUsed)}</div>
						</div>
						<div class="stat-title">Hints</div>
						<div class="stat-value">{numOfHints}</div>
						<div class="stat-desc"></div>
					</div>
				</td>
			</tr>
			<tr>
				<td>
					<div class="stat card shadow-xl rounded-3xl statDisplay">
						<div class="stat-figure text-secondary">
							<div class="radial-progress" style="--value:70;" role="progressbar">{puzzleCompleted / (numOfGiveUpsUsed + puzzleCompleted)}</div>
						</div>
						<div class="stat-title">Puzzles Completed</div>
						<div class="stat-value">{puzzleCompleted}</div>
						<div class="stat-desc">Puzzles completed without giving up</div>
					</div>
				</td>
				<td>
					<div class="stat card shadow-xl rounded-3xl statDisplay">
						<div class="stat-figure text-secondary">
							<div class="radial-progress" style="--value:70;" role="progressbar">{puzzleCompleted / (numOfGiveUpsUsed + puzzleCompleted)}</div>
						</div>
						<div class="stat-title">Puzzles Completed</div>
						<div class="stat-value">{puzzleCompleted}</div>
						<div class="stat-desc">Puzzles completed without giving up</div>
					</div>
				</td>
			</tr>
		</table>
	</div>
</div>


<style>
	button,input,h1,h2,tr,td,div {
		font-family: 'BadComic';
	}
</style>