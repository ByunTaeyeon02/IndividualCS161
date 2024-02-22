from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

tileGrid = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
tileGridAnswer = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

def generatePuzzle():
    clearAll()
    for row in range(0, 5):
        for column in range(0, 5):
            temp = random.randint(1, 2)
            tileGridAnswer[row][column] = temp


def clearAll():
    tileGrid = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    tileGridAnswer = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]


def clearTileGrid():
    for row in range(0, 5):
        for column in range(0, 5):
            tileGrid[row][column] = 0

def getStringDisplay():
    stringDisplay = [["", "", "", "", ""],["", "", "", "", ""]];
    topStringArr = []
    sideStringArr = []
    for index in range(0, 5):
        topStringArr.append(getRowString(index))
        sideStringArr.append(getColumnString(index))

    for index in range(0, 5):
        top = topStringArr[index].split(" ")
        side = sideStringArr[index].split(" ")
        topCur = 0
        sideCur = 0
        topString = ""
        sideString = ""
		
        for element in top:
            if element == 1:
                topCur += 1
            else:
                if topCur != 0:
                    topString += topCur + "\n"
                topCur = 0
                
        for element in side:
            if element == 1:
                sideCur += 1
            else:
                if sideCur != 0:
                    sideString += sideCur + " "
                sideCur = 0

        if topCur != 0:
            topString += topCur + "\n"
        if sideCur != 0:
            sideString += sideCur + " "
        stringDisplay[0][index] = stringDisplay[0][index] + topString
        stringDisplay[1][index] = stringDisplay[1][index] + sideString
    return stringDisplay

def getTopRow():
    arr = []
    for column in range(0, 5):
        arr.append(getRowString(column))
    return arr

def getSideRow():
    arr = []
    for row in range(0, 5):
        arr.append(getColumnString(row))
    return arr


def getColumnString(curRow):
    column_string  = ""
    for column in range(len(tileGridAnswer[curRow])):
        column_string  += str(tileGridAnswer[curRow][column]) + " "
    return column_string .strip()


def getRowString(curCol):
    row_string = ""
    for row in range(len(tileGridAnswer)):
        row_string += str(tileGridAnswer[row][curCol]) + " "
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

@app.route('/getStringRowArr')
def getStringRowArr():
    return jsonify({'topColArr': getTopRow(), 'sideRowArr': getSideRow()})

@app.route('/getStringRowArr1')
def getStringRowArr1():
    displayString = getStringDisplay()
    return jsonify({'topColArr': displayString[0], 'sideRowArr': displayString[1]})

if __name__ == '__main__':
    app.run(debug=True, port=8080)