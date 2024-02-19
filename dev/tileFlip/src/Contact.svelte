<script lang="ts">
	export let tileGrid = [[0, 0, 0, 0, 0], 
						   [0, 0, 0, 0, 0], 
						   [0, 0, 0, 0, 0], 
						   [0, 0, 0, 0, 0], 
						   [0, 0, 0, 0, 0]];
	function toggleColor(row , col) {
		tileGrid[row][col] += 1;
		if (tileGrid[row][col] > 2) {
			tileGrid[row][col] = 0;
		}
	  }
	console.log(tileGrid[0][0]);
</script>

<style>
	.tile {
		width: 100px;
		height: 100px;
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
</style>

<html lang="ts">
	<table class="grid">
		{#each tileGrid as row, rowIndex}
			<tr>
				{#each row as value, colIndex}
					<td>
						<button class="btn tile" class:gray={value === 0} class:white={value === 1} class:black={value === 2} on:click={() => toggleColor(rowIndex, colIndex)}>
							{value === 0 ? '' : (value === 1 ? 'W' : 'B')}
						</button>
					</td>
				{/each}
			</tr>
		{/each}
	</table>
</html>