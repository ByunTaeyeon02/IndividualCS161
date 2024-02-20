<script lang="ts">
	import { onMount } from 'svelte';
	let tileGrid = [];
	async function fetchData() {
		try {
			const response = await fetch('http://localhost:5000/generateNewPuzzle');
			const data = await response.json();
			tileGrid = data.tileGrid;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function showSolution() {
		try {
			const response = await fetch('http://localhost:5000/showSolution');
			const data = await response.json();
			tileGrid = data.tileGridAnswer;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function resetTileGrid() {
		try {
			const response = await fetch('http://localhost:5000/resetGrid');
			const data = await response.json();
			tileGrid = data.tileGrid;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}
	
	onMount(() => {
		fetchData();
	});

	function toggleColor(row , col) {
		const currentValue = tileGrid[row][col];
		if (typeof currentValue === 'number') {
			tileGrid[row][col] += 1;
			if (tileGrid[row][col] > 2) {
				tileGrid[row][col] = 0;
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
			{#each tileGrid as row, rowIndex}
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
		<button class="btn btn-success">Check Answer</button>
		<button class="btn btn-warning">Get Hint</button>
	</div>
</html>