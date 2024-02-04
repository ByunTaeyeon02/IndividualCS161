+ Project Title:
    + Tile Flip
+ GitHub URL:
    + https://github.com/ByunTaeyeon02/IndividualCS161
+ Milestones with deadlines:
    + M1 (2/6 - 2/15): Setting up Github and Flask App
    + M2 (2/20 - 2/29): Add log-in, sign-up, and log-out
    + M3 (3/5 - 3/14): Build 5x5 tiles and generate patterns
    + M4 (3/19 - 3/28): Add “flippable” tiles and a record number of incorrect flips
    + M5 (4/2 - 4/11): Implement an algorithm to solve tile without using help from the database
    + M6 (4/16 - Finals): Testing for bugs and making visuals a little bit better
+ Front-end and back-end technologies:
    + Front-end: Svelte, Tailwind, Javascript, CSS, HTML
    + Back-end: Flask, Python
+ Algorithms/AI schemes used in the core engine:
    + Generating Puzzle: for each tile in the 5x5, use a random number generator to determine if the square is black or white
    + Solver:
        + Start with the highest numbered "line" and flip in the possible tiles to black
            + Ex: a line with 4 would mean that the center 3 out of 5 tiles will need to be flip
        + Once there are no more lines that are higher than 3, go through each line and mark the tiles as white if number conditions are meet
            + Ex: if the number condition for the line is 5 and all 5 tiles on that line are black then the line is done
            + Ex 2: if the line is 3 and three of the five tiles are black then mark the other 2 non-black tiles as white
        + If a line has a a black tile next to a white one then starting from that black tile add n - 1 numbers of tile (n being the number condition)
            + Ex: let w be white and b be black and g be gray (unmarked):
                + If n is 3: w b u u u  -->  w b b b w
                + If n is 4: w b u u u  -->  w b b b b
+ Marketspace / Selling point:
    + A 5x5 simple tile game with free hints

