from flask import Flask, jsonify, request, render_template, redirect, session, url_for, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_session import Session
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    userType = db.Column(db.String(100), nullable=False)
    darkModeOn = db.Column(db.Boolean, nullable=False)
    puzzleCompleted = db.Column(db.Integer, nullable=False)
    numOfHints = db.Column(db.Integer, nullable=False)
    numOfHintsUsed = db.Column(db.Integer, nullable=False)
    numOfGiveUpsUsed = db.Column(db.Integer, nullable=False)

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

@app.route('/favicon.ico')
def favicon():
     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def base():
    static_directory = os.path.join(os.getcwd(), 'dev', 'client', 'build')
    return send_from_directory(static_directory, 'index.html')

@app.route("/<path:path>")
def home(path):
    static_directory = os.path.join(os.getcwd(), 'dev', 'client', 'build')
    return send_from_directory(static_directory, path)

@app.route('/protected')
def protected():
    if current_user.is_authenticated:
        return jsonify({'loggedIn': True})
    else:
        return jsonify({'loggedIn': False})

@app.route('/current_user_id')
@login_required
def current_user_id():
    return jsonify({'user_id': current_user.id})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    userType = "Regular User"
    darkModeOn = data.get('darkModeOn')
    puzzleCompleted = 0
    numOfHints = 10
    numOfHintsUsed = 0
    numOfGiveUpsUsed = 0
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, userType=userType,
                darkModeOn=darkModeOn, puzzleCompleted=puzzleCompleted, 
                numOfHints=numOfHints, numOfHintsUsed=numOfHintsUsed,
                numOfGiveUpsUsed=numOfGiveUpsUsed)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        if current_user.is_authenticated:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Failed to log in'})
    return jsonify({'message': 'Invalid username or password'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route("/getDarkMode")
@login_required
def getDarkMode():
    if current_user.is_authenticated:
        return jsonify({'darkModeOn': current_user.darkModeOn})
    else:
        return jsonify({'message': 'User not authenticated'}), 401

@app.route("/setDarkMode", methods=['POST'])
@login_required
def setDarkMode():
    if current_user.is_authenticated:
        data = request.get_json()
        darkModeOn = data.get('darkModeOn')
        current_user.darkModeOn = darkModeOn
        db.session.commit()
        return jsonify({'darkModeOn': current_user.darkModeOn})
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
@app.route("/getPuzzleCompleted")
@login_required
def getPuzzleCompleted():
    if current_user.is_authenticated:
        return jsonify({'puzzleCompleted': current_user.puzzleCompleted})
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
@app.route("/setPuzzleCompleted", methods=['POST'])
@login_required
def setPuzzleCompleted():
    if current_user.is_authenticated:
        data = request.get_json()
        puzzleCompleted = data.get('puzzleCompleted')
        current_user.puzzleCompleted = puzzleCompleted
        db.session.commit()
        return jsonify({'puzzleCompleted': current_user.puzzleCompleted})
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
@app.route("/getNumOfHints")
@login_required
def getNumOfHints():
    if current_user.is_authenticated:
        return jsonify({'numOfHints': current_user.numOfHints})
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
@app.route("/setNumOfHints", methods=['POST'])
@login_required
def setNumOfHints():
    if current_user.is_authenticated:
        data = request.get_json()
        numOfHints = data.get('numOfHints')
        current_user.numOfHints = numOfHints
        db.session.commit()
        return jsonify({'message': str(numOfHints) + ' added'})
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
@app.route("/getNumOfHintsUsed")
@login_required
def getNumOfHintsUsed():
    if current_user.is_authenticated:
        return jsonify({'numOfHintsUsed': current_user.numOfHintsUsed})
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
@app.route("/setNumOfHintsUsed", methods=['POST'])
@login_required
def setNumOfHintsUsed():
    if current_user.is_authenticated:
        data = request.get_json()
        numOfHintsUsed = data.get('numOfHintsUsed')
        current_user.numOfHintsUsed = numOfHintsUsed
        db.session.commit()
        return jsonify({'numOfHintsUsed': current_user.numOfHintsUsed})
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
@app.route("/getNumOfGiveUpsUsed")
@login_required
def getNumOfGiveUpsUsed():
    if current_user.is_authenticated:
        return jsonify({'numOfGiveUpsUsed': current_user.numOfGiveUpsUsed})
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
@app.route("/setNumOfGiveUpsUsed", methods=['POST'])
@login_required
def setNumOfGiveUpsUsed():
    if current_user.is_authenticated:
        data = request.get_json()
        numOfGiveUpsUsed = data.get('numOfGiveUpsUsed')
        current_user.numOfGiveUpsUsed = numOfGiveUpsUsed
        db.session.commit()
        return jsonify({'numOfGiveUpsUsed': current_user.numOfGiveUpsUsed})
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
@app.route("/getUserInfo")
@login_required
def getUserInfo():
    if current_user.is_authenticated:
        return jsonify({'username': current_user.username, 
                        'userType': current_user.userType,
                        'darkModeOn': current_user.darkModeOn,
                        'puzzleCompleted': current_user.puzzleCompleted,
                        'numOfHints': current_user.numOfHints,
                        'numOfHintsUsed': current_user.numOfHintsUsed,
                        'numOfGiveUpsUsed': current_user.numOfGiveUpsUsed,})
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
@app.route("/setUsername", methods=['POST'])
@login_required
def setUsername():
    if current_user.is_authenticated:
        data = request.get_json()
        username = data.get('username')
        current_user.username = username
        db.session.commit()
        return jsonify({'username': current_user.username})
    else:
        return jsonify({'message': 'User not authenticated'}), 401
    
@app.route("/setPassword", methods=['POST'])
@login_required
def setPassword():
    if current_user.is_authenticated:
        data = request.get_json()
        password = data.get('password')
        current_user.password = password
        db.session.commit()
        return jsonify({'password': current_user.password})
    else:
        return jsonify({'message': 'User not authenticated'}), 401

@app.route('/generateNewPuzzle')
def generateNewPuzzle():
    generatePuzzle()
    return jsonify({'tileGrid': tileGrid})

@app.route('/getStringRowArr')
def getStringRowArr():
    return jsonify({'topColArr': getTopRow(), 'sideRowArr': getSideRow()})

@app.route('/getStringRowArr1')
def getStringRowArr1():
    displayString = getStringDisplay()
    return jsonify({'topColArr': displayString[0], 'sideRowArr': displayString[1]})

@app.route('/showSolution')
def showSolution():
    return jsonify({'tileGridAnswer': tileGridAnswer})

@app.route('/resetGrid')
def resetGrid():
    clearTileGrid()
    return jsonify({'tileGrid': tileGrid})

@app.route('/getHint', methods=['POST'])
def getHint():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')
    value = tileGridAnswer[row - 1][col - 1]
    return jsonify({'value': value})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)