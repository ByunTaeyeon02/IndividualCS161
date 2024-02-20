from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

tileGrid = [
    [" ", "", "", "", "", ""],
    ["", 0, 0, 0, 0, 0],
    ["", 0, 0, 0, 0, 0],
    ["", 0, 0, 0, 0, 0],
    ["", 0, 0, 0, 0, 0],
    ["", 0, 0, 0, 0, 0]
]

tileGridAnswer = [
    [" ", "", "", "", "", ""],
    ["", 0, 0, 0, 0, 0],
    ["", 0, 0, 0, 0, 0],
    ["", 0, 0, 0, 0, 0],
    ["", 0, 0, 0, 0, 0],
    ["", 0, 0, 0, 0, 0]
]

"""
 [" ", "1\n1\n1\n", "3\n", "1\n3\n", "2\n", "4\n"],
    ["1\n1\n1\n", 0, 0, 0, 0, 0],
    ["1\n2\n", 0, 0, 0, 0, 0],
    ["5\n", 0, 0, 0, 0, 0],
    ["2\n1\n", 0, 0, 0, 0, 0],
    ["1\n1\n", 0, 0, 0, 0, 0]
"""

def generatePuzzle():
    clearTileGrid()
    for row in range(1, 6):
        for column in range(1, 6):
            temp = random.randint(1, 2)
            tileGridAnswer[row][column] = temp

    for column in range(1, 6):
        tileGridAnswer[0][column] = getColumnString()
        tileGrid[0][column] = tileGridAnswer[0][column]

    for row in range(1, 6):
        tileGridAnswer[row][0] = getRowString()
        tileGrid[row][0] = tileGridAnswer[row][0]  

def clearTileGrid():
    for row in range(1, 6):
        for column in range(1, 6):
            tileGrid[row][column] = 0

def getColumnString():
    string = "C"
    return string

def getRowString():
    string = "R"
    return string


@app.route('/generateNewPuzzle')
def generateNewPuzzle():
    generatePuzzle()
    return jsonify({'tileGrid': tileGrid})

@app.route('/showSolution')
def showSolution():
    return jsonify({'tileGridAnswer': tileGridAnswer})

@app.route('/resetGrid')
def resetGrid():
    clearTileGrid()
    return jsonify({'tileGrid': tileGrid})

if __name__ == '__main__':
    app.run(debug=True)