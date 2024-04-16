<script lang="ts">
	import { onMount } from 'svelte';
	
	// fetched data
	let username: string;
	let userType: string;
	let puzzleCompleted: number;
	let numOfHints: number;
	let numOfHintsUsed: number;
	let numOfGiveUpsUsed: number;

	let allPuzzleCompleted: number;
	let allNumOfHints: number;
	let allNumOfHintsUsed: number;
	let allNumOfGiveUpsUsed: number;

	let topFive = [["p1", 100, 25, 0, 1],
					["p2", 80, 35, 10, 1],
					["p3", 75, 15, 0, 1],
					["p4", 20, 7, 5, 1],
					["p5", 10, 4, 4, 1]];

	async function fetchTotal() {
        try {
            const response = await fetch('/getTotals');
            if (!response.ok) {
                throw new Error('Failed to fetch totals');
            }
            const data = await response.json();
            allPuzzleCompleted = data.total_puzzle_completed;
            allNumOfHints = data.total_num_of_hints;
            allNumOfHintsUsed = data.total_num_of_hints_used;
            allNumOfGiveUpsUsed = data.total_num_of_give_ups_used;
        } catch (error) {
            console.error(error);
        }
    }

	async function updateTopFive() {
        try {
            const response = await fetch('/getTopScores');
            if (!response.ok) {
                throw new Error('Failed to fetch top scores');
            }
            const data = await response.json();
            topFive = data;
			console.log(topFive);
        } catch (error) {
            console.error(error);
        }
    }

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
		updateTopFive();
		fetchTotal();
	});

	function formatPercentage(number: number) {
        return (number * 100).toFixed(2);
    }
</script>

<svelte:head>
	<title>Score</title>
</svelte:head>

<div class="text-column">
	<div>
		<div class="pt-2"></div>

		<h2>Your Score</h2>
		<div class="stat card shadow-xl rounded-3xl statDisplay pt-8">
			<div class="stat-figure text-secondary">
				<div class="radial-progress" style="--value:{formatPercentage(numOfGiveUpsUsed / (numOfGiveUpsUsed + puzzleCompleted))};" role="progressbar">
					{formatPercentage(numOfGiveUpsUsed / (numOfGiveUpsUsed + puzzleCompleted))}
				</div>
			</div>
			<div class="stat-title">Puzzles Completed</div>
			<div class="stat-value">{puzzleCompleted}</div>
			<div class="stat-desc">You gave up {formatPercentage(numOfGiveUpsUsed / (numOfGiveUpsUsed + puzzleCompleted))}% of the puzzles</div>
		</div>
		<div class="stat card shadow-xl rounded-3xl statDisplay pt-8">
			<div class="stat-figure text-secondary">
				<div class="radial-progress" style="--value:{formatPercentage(numOfHintsUsed / (numOfHints + numOfHintsUsed))};" role="progressbar">
					{formatPercentage(numOfHintsUsed / (numOfHints + numOfHintsUsed))}
				</div>
			</div>
			<div class="stat-title">Number of Hints Used</div>
			<div class="stat-value">{numOfHintsUsed}</div>
			<div class="stat-desc">You used {formatPercentage(numOfHintsUsed / (numOfHints + numOfHintsUsed))}% of your total hints</div>
		</div>

		<div class="pt-12"></div>

		<h2>Others' Scores</h2>
		<div class="stat card shadow-xl rounded-3xl statDisplay pt-8">
			<div class="stat-figure text-secondary">
				<div class="radial-progress" style="--value:{formatPercentage(allNumOfGiveUpsUsed / (allNumOfGiveUpsUsed + allPuzzleCompleted))};" role="progressbar">
					{formatPercentage(allNumOfGiveUpsUsed / (allNumOfGiveUpsUsed + allPuzzleCompleted))}
				</div>
			</div>
			<div class="stat-title">Puzzles Completed</div>
			<div class="stat-value">{allPuzzleCompleted}</div>
			<div class="stat-desc">Others gave up {formatPercentage(allNumOfGiveUpsUsed / (allNumOfGiveUpsUsed + allPuzzleCompleted))}% of the puzzles</div>
		</div>
		<div class="stat card shadow-xl rounded-3xl statDisplay pt-8">
			<div class="stat-figure text-secondary">
				<div class="radial-progress" style="--value:{formatPercentage(allNumOfHintsUsed / (allNumOfHints + allNumOfHintsUsed))};" role="progressbar">
					{formatPercentage(allNumOfHintsUsed / (allNumOfHints + allNumOfHintsUsed))}
				</div>
			</div>
			<div class="stat-title">Number of Hints Used</div>
			<div class="stat-value">{allNumOfHintsUsed}</div>
			<div class="stat-desc">Others used {formatPercentage(allNumOfHintsUsed / (allNumOfHints + allNumOfHintsUsed))}% of their total hints</div>
		</div>

		<div class="pt-12"></div>

		<div class="overflow-x-auto overflow-y-auto" style="max-height: 25vh;">
			<table class="table table-pin-rows">
				<thead>
					<tr>
						<th></th>
						<th>Username</th>
						<th>Puzzles Completed</th>
						<th>Hints Stored</th>
						<th>Hints Used</th>
						<th>Give Ups</th>
					</tr>
				</thead>
				<tbody id="tableBody">
					{#each topFive as row, rowIndex}
						<tr class="hover">
							<th>{rowIndex + 1}</th>
							{#each row as value, colIndex}
								<td>{value}</td>
							{/each}
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>

<style>
	
</style>