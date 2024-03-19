from flask import Flask, jsonify, request, render_template, redirect, session, url_for, send_from_directory
from flask_cors import CORS
import random

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin

from flask_session import Session

# app = Flask(__name__, static_folder='../client/src')
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
    darkModeOn = db.Column(db.Boolean, nullable=False)

@app.route('/current_user_id')
@login_required
def current_user_id():
    return jsonify({'user_id': current_user.id})

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    darkModeOn = data.get('darkModeOn')
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, darkModeOn=darkModeOn)
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
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/protected')
def protected():
    if current_user.is_authenticated:
        return jsonify({'loggedIn': True})
    else:
        return jsonify({'loggedIn': False})




# testing grabing without http
@app.route("/")
def base():
    return send_from_directory('../client/build', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('../client/build', path)

@app.route("/getDarkMode")
def getDarkMode():
    if current_user.is_authenticated:
        return jsonify({'darkModeOn': current_user.darkModeOn})
    else:
        return jsonify({'message': 'User not authenticated'}), 401

@app.route("/setDarkMode", methods=['POST'])
def setDarkMode():
    if current_user.is_authenticated:
        data = request.get_json()
        darkModeOn = data.get('darkModeOn')
        current_user.darkModeOn = darkModeOn
        db.session.commit()
        return jsonify({'darkModeOn': current_user.darkModeOn})
    else:
        return jsonify({'message': 'User not authenticated'}), 401


'''
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
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
        session['logged_in'] = True
        session['username'] = user.username
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid username or password'})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully'})

'''



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


def getHintSquare(row,col):
    return tileGridAnswer[row][col]



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
    app.run(debug=True, port=8080)