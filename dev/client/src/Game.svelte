<script lang="js">
	import { onMount } from 'svelte';

	let DisplayedGrid = [
		[" ", "", "", "", ""],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0]
	]
	let tileGrid = [];
	async function generatePuzzle() {
		try {
            const response = await fetch('http://127.0.0.1:8080/generateNewPuzzle');
			const data = await response.json();
			tileGrid = data.tileGrid;
			translateTileToDisplay();
            console.log(tileGrid);
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
            console.log(tileGrid);
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
				DisplayedGrid[row][col] = tileGrid[row - 1][col - 1]
			}
		}
	}

	let topStringArr = []
	let sideStringArr = []
	async function getStringDisplay() {
		try {
			const response = await fetch('http://127.0.0.1:8080/getStringRowArr');
			const data = await response.json();
			topStringArr = data.topColArr;
			sideStringArr = data.sideRowArr;
			console.log(topStringArr);
			console.log(sideStringArr);
			setStringDisplay();
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}
	function setStringDisplay() {
		for (let index = 0; index < 5; index++) {
			let top = topStringArr[index].split(" ");
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

	function toggleColor(row , col) {
		const currentValue = DisplayedGrid[row][col];
		if (typeof currentValue === 'number') {
			DisplayedGrid[row][col] += 1;
			if (DisplayedGrid[row][col] > 2) {
				DisplayedGrid[row][col] = 0;
			}
		}
	}
</script>

<style>
	.tile {
		width: 7.5vw;
		height: 7.5vw;
		align-items: center;
		margin: 0;
		padding: 0;
	}

	.grid {
		border-collapse: collapse;
	}

	.gray {
		background-color: #ccc;
	}

	.black {
		background-color: #000;
	}

	.white {
		background-color: #fff;
	}

	.top {
		white-space: pre;
	}

	.side {
		text-align: right;
	}
</style>

<html lang="ts">
	<div>
		<table class="grid">
			{#each DisplayedGrid as row, rowIndex}
				<tr>
					{#each row as value, colIndex}
						{#if rowIndex === 0}	
							<td style="vertical-align: bottom; text-align: center">
								<span class="top">{value}</span>
							</td>
						{:else}
							<td style="text-align: right">
								{#if typeof value === 'number'}
									<button class="btn tile" class:gray={value === 0} class:black={value === 1} class:white={value === 2} on:click={() => toggleColor(rowIndex, colIndex)}></button>
								{:else}
									<span class="side">{value}</span>
								{/if}
							</td>
						{/if}
					{/each}
				</tr>
			{/each}
		</table>
		<button class="btn btn-error" on:click={showSolution}>Show Solution</button>
		<button class="btn btn-success" on:click={generatePuzzle}>Check Answer</button>
		<button class="btn btn-warning">Get Hint</button>
	</div>
</html>