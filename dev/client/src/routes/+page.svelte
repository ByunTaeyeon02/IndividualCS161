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
	let finished = false;

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
			finished = false;
			checksLeft = 3;
			showSolutionAnswer = false;
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
			console.log("showSolution tileGrid: " + tileGrid);
			console.log("showSolution DisplayedGrid: " + DisplayedGrid);
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
		if (!gaveUp || !finished) {
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
			checkAnswer2();
		}
	}

	function checkAnswer2() {
		let correct = true;

		for (let i = 1; i <= 5; i++) {
			correct = correct && checkCol(i);
			//console.log(checkCol(i));
		}

		for (let i = 1; i <= 5; i++) {
			correct = correct && checkRow(i);
			//console.log(checkRow(i));
		}

		if (correct) {
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
			finished = true;
			//console.log(numOfHints);
		} else {
			showRightAnswerMsg = false;
			showWrongAnswerMsg = true;
			checksLeft -= 1;
			wrongAnswerMsg = (checksLeft + " checks left");
			if (checksLeft == 0) {
				showSolution();
			}
		}
	}

	function checkRow(col: number) {
		let checkString = DisplayedGrid[col][0];
		let rowAnswer = "";
		for (let i = 1; i <= 5; i++) {
			rowAnswer += DisplayedGrid[col][i];
		}
		//console.log(checkString + " : " + rowAnswer);
		
		let splittedArray = checkString.toString().split(" ");
		let regex = "^2*";
		for (let i = 0; i < splittedArray.length - 1; i++) {
			regex += `1{${splittedArray[i]}}`;
			if (i != splittedArray.length - 2) {
				regex += "2+";
			}
		}
		regex += "2*$"; 

		const regexPattern = new RegExp(regex);
		if (regexPattern.test(rowAnswer)) {
			return true;
		} else {
			return false;
		}
	}

	function checkCol(row: number) {
		let checkString = DisplayedGrid[0][row];
		let colAnswer = "";
		for (let i = 1; i <= 5; i++) {
			colAnswer += DisplayedGrid[i][row];
		}
		//console.log(checkString + " : " + colAnswer);

		let splittedArray = checkString.toString().split("\n");
		let regex = "^2*";
		for (let i = 0; i < splittedArray.length - 1; i++) {
			regex += `1{${splittedArray[i]}}`;
			if (i != splittedArray.length - 2) {
				regex += "2+";
			}
		}
		regex += "2*$"; 

		const regexPattern = new RegExp(regex);
		//console.log(regexPattern);
		if (regexPattern.test(colAnswer)) {
			return true;
		} else {
			return false;
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

	function toggleAnswers() {
		/*
		if (!gaveUp) {
			showSolution();
		}
		*/
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
	<div class="gameScreen pb-20">
		<div class="card shadow-xl tileBoardPadding rounded-3xl">
			<div class="card-body">
				<table style="border-collapse: collapse;">
					{#each DisplayedGrid as row, rowIndex}
						<tr>
							{#each row as value, colIndex}
								{#if rowIndex === 0}	
									<td style="vertical-align: bottom; text-align: center;">
										<span class="top displayTableString">{value}</span>
									</td>
								{:else}
									<td style="text-align: right;">
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
					{:else if finished}
						<tr class="pt-2">
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
				<div>
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
	<dialog id="tutorial" class="modal">
		<div class="modal-box w-8/10 max-w-5xl">
			<form method="dialog">
				<button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
			</form>
			<div>
				<p class="font-bold text-2xl">Tutorial</p>
				<table>
					<tr>
						<td><div class="pb-2"></div></td>
					</tr>
					<tr>
						<td colspan="2" class="font-bold">Game:</td>
					</tr>
					<tr>
						<td><p>+ You are trying to color the tiles based on the rules in the rows/columns</p></td>
					</tr>
					<tr>
						<td><p>+ Ex: if the row rule states "4" then that means that for that row there will be 4 black tiles with no space in between</p></td>
					</tr>
					<tr>
						<td>
							<table style="border-collapse: collapse;">
								<tr style="text-align: right;">
									<td><span class="side displayTableString pr-5">4</span></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl white"></button></td>
								</tr>
								<tr style="text-align: right;">
									<td><span class="side displayTableString pr-5">4</span></td>
									<td><button class="btn tile shadow-xl white"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
								</tr>
							</table>
						</td>
					</tr>
					<tr>
						<td><p>+ Ex: if the row rule states "1 2" then that means that for that row there will be 1 black tiles follow by atleast 1 white square and then another 2 black tiles</p></td>
					</tr>
					<tr>
						<td>
							<table style="border-collapse: collapse;">
								<tr style="text-align: right;">
									<td><span class="side displayTableString pr-5">1 2</span></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl white"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl white"></button></td>
								</tr>
								<tr style="text-align: right;">
									<td><span class="side displayTableString pr-5">1 2</span></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl white"></button></td>
									<td><button class="btn tile shadow-xl white"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
								</tr>
								<tr style="text-align: right;">
									<td><span class="side displayTableString pr-5">1 2</span></td>
									<td><button class="btn tile shadow-xl white"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl white"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
									<td><button class="btn tile shadow-xl black"></button></td>
								</tr>
							</table>
						</td>
					</tr>
					<tr>
						<td><div class="pb-4"></div></td>
					</tr>
					<tr>
						<td colspan="2" class="font-bold">Interactables:</td>
					</tr>
					<tr>
						<td><p>+ Tiles: Click on tiles to flip and change color</p></td>
					</tr>
					<tr>
						<td><p>+ Give up: Click show solution</p></td>
					</tr>
					<tr>
						<td><p>+ Reset: Click to reset all tiles to gray</p></td>
					</tr>
					<tr>
						<td><p>+ Hint: Select a tile after pressing hint button to see solution for that tile</p></td>
					</tr>
					<tr>
						<td><p>+ Check: Click to check answer</p></td>
					</tr>
				</table>
			</div>
		</div>
	</dialog>
</html>

<style>
	@import 'tailwindcss/base';
	@import 'tailwindcss/components';
	@import 'tailwindcss/utilities';

	.tileBoardPadding {
		padding-right: 4vw;
		padding-top: 2vh;
	}

	.stats {
		width: 85vw;
		max-width: 500px;
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
		width: 8vw;
		height: 7vw;
		border-radius: 10px 20px;
		min-width: 55px;
		max-width: 75px;
		max-height: 55px;
		font-size: small;
	}

	.middleBut {
		width: 6.5vw;
		height: 3vw;
		border-radius: 20px;
		min-width: 45px;
		max-width: 65px;
		max-height: 40px;
		font-size: small;
	}

	.check {
		width: 8vw;
		height: 7vw;
		border-radius: 20px 10px;
		min-width: 55px;
		max-width: 75px;
		max-height: 55px;
		font-size: small;
	}

	.gameScreen {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding-top: 5vh;
	}

	.displayTableString {
		font-size: medium;
	}

	.tile {
		width: 6vw;
		height: 6vw;
		align-items: center;
		margin: 0;
		padding: 0;
		min-width: 50px;
		min-height: 50px;
		max-width: 60px;
		max-height: 60px;
	}

	.padding {
		padding-right: 0%;
		padding-bottom: 2vh;
	}

	tr {
		font-size: small;
	}

    @media (min-width: 1300px) {
		.gameScreen {
			flex-direction: row;
		}

		.tileBoardPadding {
			padding-right: 20px;
			padding-top: 2vh;
		}

		.padding {
			padding-right: 2vw;
			padding-bottom: 0%;
		}

		tr {
			font-size: medium;
		}

        .tile {
			width: 4vh;
			height: 4vh;
			min-width: 60px;
			min-height: 60px;
			max-width: 70px;
			max-height: 70px;
		}

		.giveUp {
			width: 5vw;
			height: 4vw;
			border-radius: 15px 25px;
			max-width: 65px;
			max-height: 65px;
			font-size: medium;
		}

		.middleBut {
			width: 3.5vw;
			height: 1vw;
			max-width: 60px;
			max-height: 45px;
			font-size: medium;
		}

		.check {
			width: 5vw;
			height: 4vw;
			border-radius: 25px 15px;
			max-width: 65px;
			max-height: 65px;
			font-size: medium;
		}

		.displayTableString {
			font-size: medium;
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
