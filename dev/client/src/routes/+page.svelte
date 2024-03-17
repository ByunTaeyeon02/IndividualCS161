<script lang="js">
	import { onMount } from 'svelte';

	// @ts-ignore
	let tileGrid = [];
	let DisplayedGrid = [
		[" ", "", "", "", ""],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0]
	]

	let hintOn = false;

	let gaveUp = false;

	let showWrongAnswerMsg = false;
	let showRightAnswerMsg = false;
	let showWarningMsg = false;
	let showResetMsg = false;
	let wrongAnswerMsg = "";
	let rightAnswerMsg = "";
	let warningMsg = "";
	let restMsg = "";
	
	async function generatePuzzle() {
		try {
            const response = await fetch('http://127.0.0.1:8080/generateNewPuzzle');
			const data = await response.json();
			tileGrid = data.tileGrid;
			translateTileToDisplay();
			getStringDisplay();
			showRightAnswerMsg = false;
			gaveUp = false;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function showSolution() {
		try {
			const response = await fetch('http://127.0.0.1:8080/showSolution');
			const data = await response.json();
			tileGrid = data.tileGridAnswer;
			translateTileToDisplay();
			gaveUp = true;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	// @ts-ignore
	async function getHint(row, col) {
		try {
			const response = await fetch('http://127.0.0.1:8080/getHint', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ row: row, col: col })
			});
			const data = await response.json();
			DisplayedGrid[row][col] = data.value;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function resetTileGrid() {
		try {
			const response = await fetch('http://127.0.0.1:8080/resetGrid');
			const data = await response.json();
			tileGrid = data.tileGrid;
			translateTileToDisplay();
			showResetMsg = false;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	function translateTileToDisplay() {
		for (let row = 1; row < 6; row++) {
			for (let col = 1; col < 6; col++) {
				// @ts-ignore
				DisplayedGrid[row][col] = tileGrid[row - 1][col - 1]
			}
		}
	}

	// @ts-ignore
	let topStringArr = []
	// @ts-ignore
	let sideStringArr = []
	async function getStringDisplay() {
		try {
			const response = await fetch('http://127.0.0.1:8080/getStringRowArr');
			const data = await response.json();
			topStringArr = data.topColArr;
			sideStringArr = data.sideRowArr;
			setStringDisplay();
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}
	function setStringDisplay() {
		for (let index = 0; index < 5; index++) {
			// @ts-ignore
			let top = topStringArr[index].split(" ");
			// @ts-ignore
			let side = sideStringArr[index].split(" ");
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
	}
	
	onMount(() => {
        generatePuzzle();
		getStringDisplay();
	});

	// @ts-ignore
	function toggleColor(row, col) {
		if (!gaveUp) {
			const currentValue = DisplayedGrid[row][col];
			if (hintOn) {
				if (typeof currentValue === 'number') { 
					getHint(row, col);
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
			const response = await fetch('http://127.0.0.1:8080/showSolution');
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
				rightAnswerMsg = "Congrats! New Puzzle?";
			} else {
				showRightAnswerMsg = false;
				showWrongAnswerMsg = true;
				wrongAnswerMsg = "Number of Incorrect Tiles: " + numWrong;
			}
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
				// @ts-ignore
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
	<title>Tile Flip Game</title>
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
					<button class="btn btn-sm btn-outline" on:click={generatePuzzle}>Accept</button>
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
					<button class="btn btn-sm btn-outline" on:click={resetTileGrid}>Accept</button>
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
		<div class="gameScreen">
			<div class="card w-300 shadow-xl pr-10 pb-6 pt-4 rounded-3xl">
				<div class="card-body">
					<table style="max-height: 90vh; overflow-y: auto; border-collapse: collapse;">
						{#each DisplayedGrid as row, rowIndex}
							<tr>
								{#each row as value, colIndex}
									{#if rowIndex === 0}	
										<td style="vertical-align: bottom; text-align: center">
											<span class="top displayTableString">{value}</span>
										</td>
									{:else}
										<td style="text-align: right">
											{#if typeof value === 'number'}
												<button class="btn tile shadow-xl" class:gray={value === 0} class:black={value === 1} class:white={value === 2} on:click={() => toggleColor(rowIndex, colIndex)}></button>
											{:else}
												<span class="side displayTableString">{value}</span>
											{/if}
										</td>
									{/if}
								{/each}
							</tr>
						{/each}
						<tr>
							<td></td>
							{#if gaveUp}
								<td colspan="5" style="text-align: center;">
									<button class="btn btn-outline shadow-xl" style=" margin-top: 2vw;" on:click={generatePuzzle}>Generate New Puzzle</button>
								</td>
							{:else}
								<td colspan="5" style="text-align: center;">
									<div style="display: flex; justify-content: space-around; margin-top: 1vw;">
										<button class="btn btn-outline btn-error giveUp shadow-xl" on:click={showSolution}>Give Up</button>
										<button class="btn btn-outline middleBut shadow-xl" on:click={confirmReset}>Reset</button>
										<div class="tooltip" data-tip="Click on a tile to see correct color">
											<input class="btn btn-outline middleBut shadow-xl" type="checkbox" bind:checked={hintOn} aria-label="Hint"/>
										</div>
										<button class="btn btn-outline btn-success check shadow-xl" on:click={checkUserAnswer}>Check</button>
									</div>
								</td>
							{/if}
						</tr>
					</table>
				</div>
			</div>
		</div>
	</section>
</html>

<style>
	@import 'tailwindcss/base';
	@import 'tailwindcss/components';
	@import 'tailwindcss/utilities';

	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
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
		border-radius: 1.5vw 3vw;
	}

	.middleBut {
		width: 7.5vw;
		height: 5vw;
		border-radius: 2vw;
	}

	.check {
		width: 9vw;
		height: 7.5vw;
		border-radius: 3vw 1.5vw;
	}

	.gameScreen {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 90vh;
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
	}

    @media (min-width: 1400px) {
        .tile {
			width: 5vw;
			height: 5vw;
		}

		.giveUp {
			width: 5.5vw;
			height: 5vw;
			border-radius: 1vw 2vw;
			font-size: 1vw;
		}

		.middleBut {
			width: 5vw;
			height: 3vw;
			border-radius: 1vw;
			font-size: 1vw;
		}

		.check {
			width: 5.5vw;
			height: 5vw;
			border-radius: 2vw 1vw;
			font-size: 1vw;
		}

		.displayTableString {
			font-size: 1.5vw;
		}
    }

	.alert {
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        width: 500px;
        z-index: 1000;
    }
</style>
