<script lang="ts">
	import { onMount } from 'svelte';

	let tileGrid: any[] = [];
	let DisplayedGrid = [
		[" ", "", "", "", ""],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0]
	]
	let userAnswerGrid = [
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0]
	]

	let hintOn = false;
	let showSolutionAnswer = false;
	let gaveUp = false;

	let showWrongAnswerMsg = false;
	let showRightAnswerMsg = false;
	let showWarningMsg = false;
	let showResetMsg = false;
	let wrongAnswerMsg = "";
	let rightAnswerMsg = "";
	let warningMsg = "";
	let restMsg = "";

	let checksLeft = 3;

	// fetched data
	let puzzleCompleted: number;
	let numOfHints: number;
	let numOfHintsUsed: number;
	let numOfGiveUpsUsed: number;

	let isLoggedIn: boolean;

	async function isUserLoggedIn() {
		try {
			const response = await fetch('/protected');
			const data = await response.json();
			isLoggedIn = data.loggedIn;
			if (isLoggedIn) {
				getUserInfoFull();
			} else {
				puzzleCompleted = 0;
				numOfHints = 10;
				numOfHintsUsed = 0;
				numOfGiveUpsUsed = 0;
			}
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function getUserInfoFull() { 
		try {
			const response = await fetch('/getUserInfo');
			const data = await response.json();
			puzzleCompleted = data.puzzleCompleted;
			numOfHints = data.numOfHints;
			numOfHintsUsed = data.numOfHintsUsed;
			numOfGiveUpsUsed = data.numOfGiveUpsUsed;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}
	
	async function generatePuzzle() {
		try {
            const response = await fetch('/generateNewPuzzle');
			const data = await response.json();
			tileGrid = data.tileGrid;
			translateTileToDisplay(tileGrid);
			getStringDisplay();
			showRightAnswerMsg = false;
			gaveUp = false;
			checksLeft = 3;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}
	
	async function showSolution() {
		try {
			const response = await fetch('/showSolution');
			const data = await response.json();
			tileGrid = data.tileGridAnswer;
			for (let row = 1; row < 6; row++) {
				for (let col = 1; col < 6; col++) {
					// @ts-ignore
					userAnswerGrid[row - 1][col - 1] = DisplayedGrid[row][col];
				}
			}
			translateTileToDisplay(tileGrid);
			if (isLoggedIn)
				addGiveUps(1);
			else
				numOfGiveUpsUsed += 1;
			gaveUp = true;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function addGiveUps(numOfGiveUpsAdded: number) {
		try {
			numOfGiveUpsUsed += numOfGiveUpsAdded;
			const response = await fetch('/setNumOfGiveUpsUsed', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({numOfGiveUpsUsed: numOfGiveUpsUsed})
			});
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function getHint(row: number, col: number) {
		try {
			const response = await fetch('/getHint', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ row: row, col: col })
			});
			const data = await response.json();
			DisplayedGrid[row][col] = data.value;
			if (isLoggedIn) {
				addHints(-1);
				addHintsUsed(1);
			} else {
				numOfHints -= 1;
				numOfHintsUsed += 1;
			}
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function addHintsUsed(numOfHintsUsedAdded: number) {
		try {
			numOfHintsUsed += numOfHintsUsedAdded;
			const response = await fetch('/setNumOfHintsUsed', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({numOfHintsUsed: numOfHintsUsed})
			});
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function resetTileGrid() {
		try {
			const response = await fetch('/resetGrid');
			const data = await response.json();
			tileGrid = data.tileGrid;
			translateTileToDisplay(tileGrid);
			showResetMsg = false;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	function translateTileToDisplay(grid: number[][]) {
		for (let row = 1; row < 6; row++) {
			for (let col = 1; col < 6; col++) {
				DisplayedGrid[row][col] = grid[row - 1][col - 1]
			}
		}
	}

	let topStringArr: any[] = []
	let sideStringArr: any[] = []
	async function getStringDisplay() {
		try {
			const response = await fetch('/getStringRowArr');
			const data = await response.json();
			topStringArr = data.topColArr;
			sideStringArr = data.sideRowArr;
			for (let index = 0; index < 5; index++) {
				let top: any[] = topStringArr[index].split(" ");
				let side: any[] = sideStringArr[index].split(" ");
				let topCur = 0;
				let sideCur = 0;
				let topString = "";
				let sideString = "";
				for (let i of top) {
					if (i == 1) {
						topCur++;
					} else {
						if (topCur != 0)
							topString += topCur + "\n";
						topCur = 0;
					}
				}
				for (let i of side) {
					if (i == 1) {
						sideCur++;
					} else {
						if (sideCur != 0)
							sideString += sideCur + " ";
						sideCur = 0;
					}
				}
				if (topCur != 0)
					topString += topCur + "\n";
				if (sideCur != 0)
					sideString += sideCur + " ";
				DisplayedGrid[0][index + 1] = topString;
				DisplayedGrid[index + 1][0] = sideString;
			}
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}
	
	onMount(() => {
		isUserLoggedIn();
        generatePuzzle();
	});

	function toggleColor(row: number, col: number) {
		if (!gaveUp) {
			const currentValue = DisplayedGrid[row][col];
			if (hintOn) {
				if (numOfHints > 0) {
					if (typeof currentValue === 'number') { 
						getHint(row, col);
						hintOn = false;
					}
				} else {
					showWarningMsg = true;
					warningMsg = "No hints left";
					hintOn = false;
				}
			} else {
				if (typeof currentValue === 'number') {
					if (DisplayedGrid[row][col] == 0) {
						DisplayedGrid[row][col] = 1;
					} else if (DisplayedGrid[row][col] == 1) {
						DisplayedGrid[row][col] = 2;
					} else {
						DisplayedGrid[row][col] = 0;
					}
				}
			}
		}
	}

	async function checkAnswer() {
		try {
			const response = await fetch('/showSolution');
			const data = await response.json();
			tileGrid = data.tileGridAnswer;
			let numWrong = 0;
			for (let row = 0; row < 5; row++) {
				for (let col = 0; col < 5; col++) {
					if (tileGrid[row][col] != DisplayedGrid[row + 1][col + 1])
						numWrong++;
				}
			}
			if (numWrong == 0) {
				showRightAnswerMsg = true;
				showWrongAnswerMsg = false;
				rightAnswerMsg = "Congrats (+10 Hints)! New Puzzle?";
				if (isLoggedIn) {
					addHints(10);
					addPuzzleCompleted(1);
				} else {
					numOfHints += 10;
					puzzleCompleted += 1;
				}
				console.log(numOfHints);
			} else {
				showRightAnswerMsg = false;
				showWrongAnswerMsg = true;
				checksLeft -= 1;
				wrongAnswerMsg = "Number of Incorrect Tile(s): " + numWrong + " (" + checksLeft + " checks left)";
				if (checksLeft == 0) {
					showSolution();
				}
			}
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function addHints(numOfHintsAdded: number) {
		try {
			numOfHints += numOfHintsAdded;
			const response = await fetch('/setNumOfHints', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({numOfHints: numOfHints})
			});
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function addPuzzleCompleted(puzzleCompletedAdded: number) {
		try {
			puzzleCompleted += puzzleCompletedAdded;
			const response = await fetch('/setPuzzleCompleted', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({puzzleCompleted: puzzleCompleted})
			});
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	function denyAlert() {
		showRightAnswerMsg = false;
		showResetMsg = false;
	}

	function confirmReset() {
		showResetMsg = true;
		restMsg = "Revert all tiles to gray?";
	}

	function checkUserAnswer() {
		let uncomplete = false;
		for (let row = 0; row < 5; row++) {
			for (let col = 0; col < 5; col++) {
				if (DisplayedGrid[row + 1][col + 1] == 0)
					uncomplete = true;
			}
		}
		if (uncomplete) {
			showWarningMsg = true;
			warningMsg = "All tiles must be black or white";
		} else {
			checkAnswer();
		}
	}

	function toggleAnswers() {
		if (!gaveUp) {
			showSolution();
		}
		if (showSolutionAnswer) {
			translateTileToDisplay(tileGrid);
		} else {
			translateTileToDisplay(userAnswerGrid);
		}
	}

	$: {
		if (showWrongAnswerMsg) {
			setTimeout(() => {
				showWrongAnswerMsg = false;
			}, 2500);
		}
		if (showWarningMsg) {
			setTimeout(() => {
				showWarningMsg = false;
			}, 2500);
		}
  	} 
</script>

<svelte:head>
	<title>Tile Flip</title>
	<meta name="description" content="Game page" />
</svelte:head>

<html lang="ts">
	<div>
		{#if showRightAnswerMsg}	
			<div role="alert" class="alert shadow-xl">
				<svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
				<span>{rightAnswerMsg}</span>
				<div>
					<button class="btn btn-sm btn-ghost" on:click={denyAlert}>Deny</button>
					<button class="btn btn-sm btn-outline shadow-xl" on:click={generatePuzzle}>Accept</button>
				</div>
			</div>
		{:else if showWrongAnswerMsg}
			<div role="alert" class="alert alert-error shadow-xl">
				<svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
				<span>{wrongAnswerMsg}</span>
			</div>
		{:else if showResetMsg}
			<div role="alert" class="alert shadow-xl">
				<svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
				<span>{restMsg}</span>
				<div>
					<button class="btn btn-sm btn-ghost" on:click={denyAlert}>Deny</button>
					<button class="btn btn-sm btn-outline " on:click={resetTileGrid}>Accept</button>
				</div>
			</div>
		{:else if showWarningMsg}
			<div role="alert" class="alert shadow-xl">
				<svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
				<span>{warningMsg}</span>
			</div>
		{/if}
	</div>
	<section>
		<div class="gameScreen pb-20 pt-20">
			<div class="card shadow-xl pr-10 pb-6 pt-4 rounded-3xl">
				<div class="card-body">
					<table style="border-collapse: collapse;">
						{#each DisplayedGrid as row, rowIndex}
							<tr>
								{#each row as value, colIndex}
									{#if rowIndex === 0}	
										<td style="vertical-align: bottom; text-align: center; width: auto;">
											<span class="top displayTableString">{value}</span>
										</td>
									{:else}
										<td style="text-align: right; width: auto;">
											{#if typeof value === 'number'}
												<button class="btn tile shadow-xl" class:gray={value === 0} class:black={value === 1} class:white={value === 2} on:click={() => toggleColor(rowIndex, colIndex)}></button>
											{:else}
												<span class="side displayTableString pr-5">{value}</span>
											{/if}
										</td>
									{/if}
								{/each}
							</tr>
						{/each}
						{#if gaveUp}
							<tr>
								<td></td>
								<td colspan="5" style="text-align: center;">
									<div class="form-control">
										<label class="label cursor-pointer">
										  <span class="label-text">Correct Solution</span> 
										  <input type="checkbox" class="toggle toggle-lg" bind:checked={showSolutionAnswer} on:click={toggleAnswers}/>
										  <span class="label-text">Your Answer</span> 
										</label>
									</div>
								</td>
							</tr>
							<tr>
								<td></td>
								<td colspan="5" style="text-align: center;">
									<div>
										<button class="btn btn-outline shadow-xl" style="width: 100%" on:click={generatePuzzle}>Generate New Puzzle</button>
									</div>
								</td>
							</tr>
						{:else}
							<tr>
								<td></td>
								<td colspan="5" style="text-align: center;">
									<div style="display: flex; justify-content: space-around; margin-top: 1vw;">
										<button class="btn btn-outline giveUp shadow-xl" on:click={showSolution}>Give Up</button>
										<button class="btn btn-outline middleBut shadow-xl" on:click={confirmReset}>Reset</button>
										<div class="tooltip" data-tip="Click on a tile to see correct color">
											<input class="btn btn-outline middleBut shadow-xl" type="checkbox" bind:checked={hintOn} aria-label="Hint"/>
										</div>
										<button class="btn btn-outline check shadow-xl" on:click={checkUserAnswer}>Check</button>
									</div>
								</td>
							</tr>
						{/if}
					</table>
				</div>
			</div>
			<div class="padding"></div>
			<div class="text-center" style="display: flex; flex-direction: column;">
				<div class="card shadow-xl pl-5 pb-4 pt-4 rounded-3xl stats">
					<div class="overflow-x-auto">
						<table class="table" style="width: 100%;">
							<tbody>
								<tr>
									<th>User Type</th>
									{#if isLoggedIn}
										<td>Regular User</td>
									{:else}
										<td>Guest: progress not saved</td>
									{/if}
								</tr>
								<tr>
									<th>Checks Left</th>
									<td>{checksLeft}</td>
								</tr>
								<tr>
									<th>Puzzle(s) Completed</th>
									<td>{puzzleCompleted}</td>
								</tr>
								<tr>
									<th>Hint(s) Left</th>
									<td>{numOfHints}</td>
								</tr>
								<tr>
									<th>Hint(s) Used</th>
									<td>{numOfHintsUsed}</td>
								</tr>
								<tr>
									<th>Give Up(s)</th>
									<td>{numOfGiveUpsUsed}</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
				<button class="btn btn-link" onclick="tutorial.showModal()">Click here to learn how to play</button>
			</div>
		</div>
	</section>
	<dialog id="tutorial" class="modal">
		<div class="modal-box">
			<form method="dialog">
				<button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
			</form>
			<div>
				<p class="font-bold text-xl">Tutorial</p>
			</div>
		</div>
	</dialog>
</html>

<style>
	@import 'tailwindcss/base';
	@import 'tailwindcss/components';
	@import 'tailwindcss/utilities';

	.stats {
		width: 85vw;
		max-width: 500px;
	}

	button,span,input {
		font-family: 'BadComic';
	}

	section {
		flex: 0.4;
	}

	.gray {
		background-color: gray;
	}

	.black {
		background-color: black;
	}

	.white {
		background-color: white;
	}

	.top {
		white-space: pre;
	}

	.side {
		text-align: right;
	}

	.giveUp {
		width: 9vw;
		height: 7.5vw;
		border-radius: 10px 20px;
		min-width: 75px;
		max-width: 90px;
		max-height: 75px;
	}

	.middleBut {
		width: 6.5vw;
		height: 4vw;
		border-radius: 20px;
		min-width: 70px;
		max-width: 75px;
		min-width: 50px;
	}

	.check {
		width: 9vw;
		height: 7.5vw;
		border-radius: 20px 10px;
		min-width: 75px;
		max-width: 90px;
		max-height: 75px;
	}

	.gameScreen {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		max-height: 85vh;
		overflow-y: auto;
	}

	.displayTableString {
		font-size: 2.5vw;
	}

	.tile {
		width: 8vw;
		height: 8vw;
		align-items: center;
		margin: 0;
		padding: 0;
		min-width: 60px;
		min-height: 60px;
		max-width: 75px;
		max-height: 75px;
	}

	.padding {
		padding-right: 0%;
		padding-bottom: 2vh;
	}

	tr {
		font-size: medium;
	}

    @media (min-width: 1300px) {
		.gameScreen {
			flex-direction: row;
		}

		.padding {
			padding-right: 2vw;
			padding-bottom: 0%;
		}

		tr {
			font-size: large;
		}

        .tile {
			width: 5vw;
			height: 5vw;
			max-width: 100px;
			max-height: 100px;
		}

		.giveUp {
			width: 5.5vw;
			height: 5vw;
			border-radius: 15px 25px;
			font-size: 1.25vh;
			max-width: 110px;
			max-height: 75px;
		}

		.middleBut {
			width: 5vw;
			height: 3vw;
			font-size: 1.25vh;
			max-width: 90px;
			max-height: 55px;
		}

		.check {
			width: 5.5vw;
			height: 5vw;
			border-radius: 25px 15px;
			font-size: 1.25vh;
			max-width: 110px;
			max-height: 75px;
		}

		.displayTableString {
			font-size: 1.5vw;
		}
    }

	.alert {
        position: fixed;
        top: 2vh;
        left: 50%;
        transform: translateX(-50%);
        width: 500px;
        z-index: 1000;
    }
</style>
