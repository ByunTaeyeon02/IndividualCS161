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


def generatePuzzle():
    clearAll()
    for row in range(1, 6):
        for column in range(1, 6):
            temp = random.randint(1, 2)
            tileGridAnswer[row][column] = temp

    for column in range(1, 6):
        tileGridAnswer[0][column] = getRowString(column)
        tileGrid[0][column] = tileGridAnswer[0][column]

    for row in range(1, 6):
        tileGridAnswer[row][0] = getColumnString(row)
        tileGrid[row][0] = tileGridAnswer[row][0]  


def clearAll():
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


def clearTileGrid():
    for row in range(1, 6):
        for column in range(1, 6):
            tileGrid[row][column] = 0


def getColumnString(curRow):
    """
    cur = 0
    for column in range(1, 6):
        if tileGridAnswer[row][column] == 1:
            cur += 1
        else:
            string += str(cur) + "\n"
            cur = 0

    string = str(curRow) + "\n"
    for column in range(1, 6):
        string += str(tileGridAnswer[curRow][column])
    return string
    """
    column_string  = ""
    for column in range(len(tileGridAnswer[curRow])):
        column_string  += str(tileGridAnswer[curRow][column]) + " "
    return column_string .strip()


def getRowString(curRow):
    row_string = ""
    for row in range(len(tileGridAnswer)):
        row_string += str(tileGridAnswer[row][curRow]) + " "
    return row_string.strip()


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
    app.run(debug=True, port=8080)