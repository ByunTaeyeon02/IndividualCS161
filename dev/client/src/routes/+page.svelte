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
	
	async function generatePuzzle() {
		try {
            const response = await fetch('http://127.0.0.1:8080/generateNewPuzzle');
			const data = await response.json();
			tileGrid = data.tileGrid;
			translateTileToDisplay();
			getStringDisplay();
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

	async function getStringDisplay1() {
		try {
			const response = await fetch('http://127.0.0.1:8080/getStringRowArr1');
			const data = await response.json();
			topStringArr = data.topColArr;
			sideStringArr = data.sideRowArr;
			console.log("top: " + topStringArr);
			console.log("side: " + sideStringArr);
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}
	
	onMount(() => {
        generatePuzzle();
		getStringDisplay();
		getStringDisplay1();
	});

	// @ts-ignore
	function toggleColor(row, col) {
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
			console.log(numWrong);
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}
</script>

<svelte:head>
	<title>Game</title>
	<meta name="description" content="Game page" />
</svelte:head>

<html lang="ts">
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
							<td colspan="5" style="text-align: center;">
								<div style="display: flex; justify-content: space-around; margin-top: 1vw;">
									<button class="btn btn-outline btn-error giveUp shadow-xl" on:click={showSolution}>Give Up</button>
									<div class="tooltip" data-tip="Reset color of all squares">
										<button class="btn btn-outline middleBut shadow-xl" on:click={resetTileGrid}>Reset</button>
									</div>
									<div class="tooltip" data-tip="Click on a square to see correct color">
										<input class="btn btn-outline middleBut shadow-xl" type="checkbox" bind:checked={hintOn} aria-label="Hint"/>
									</div>
									<button class="btn btn-outline btn-success check shadow-xl" on:click={checkAnswer}>Check</button>
								</div>
							</td>
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
</style>
