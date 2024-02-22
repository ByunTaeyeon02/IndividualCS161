<script lang="js">
	import { onMount } from 'svelte';
	import NavBar from './Components/NavBar.svelte';

	let tileGrid = [];
	let DisplayedGrid = [
		[" ", "", "", "", ""],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0],
		["", 0, 0, 0, 0, 0]
	]
	
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
	.grid {
		border-collapse: collapse;
	}

	.gray {
		background-color: #b5b5b5;
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

	.button {
		border: none;
		align-items: center;
		text-align: center;
		text-decoration: none;
		display: inline-block;
		font-size: 2vw;
		transition-duration: 0.4s;
		cursor: pointer;
	}

	.buttonBlack {
		background-color: #000;
		color: white;
	}

	.buttonBlack:hover {
		background-color: white;
		color: #000;
		border: 2px solid #000;
	}

	.displayTableString {
		font-size: 2.5vw;
		color: #000;
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

		.button {
			font-size: 1vw;
		}

		.giveUp {
			width: 5.5vw;
			height: 5vw;
			border-radius: 1vw 2vw;
		}

		.middleBut {
			width: 5vw;
			height: 3vw;
			border-radius: 1vw;
		}

		.check {
			width: 5.5vw;
			height: 5vw;
			border-radius: 2vw 1vw;
		}

		.displayTableString {
			font-size: 1.5vw;
		}
    }
</style>

<html lang="ts">
	<NavBar/>
	<div class="gameScreen">
		<table class="grid" style="max-height: 90vh; overflow-y: auto;">
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
									<button class="btn tile" class:gray={value === 0} class:black={value === 1} class:white={value === 2} on:click={() => toggleColor(rowIndex, colIndex)}></button>
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
						<button class="button buttonBlack giveUp" on:click={showSolution}>Give Up</button>
						<button class="button buttonBlack middleBut" on:click={resetTileGrid}>Reset</button>
						<button class="button buttonBlack middleBut">Hint</button>
						<button class="button buttonBlack check" on:click={generatePuzzle}>Done</button>
					</div>
				</td>
			</tr>
		</table>
	</div>
</html>