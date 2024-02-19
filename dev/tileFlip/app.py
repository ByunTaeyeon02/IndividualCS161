from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tileGrid_data = [
    [" ", "A", "B", "C", "D", "E"],
    ["F", 0, 0, 0, 0, 0],
    ["G", 0, 0, 0, 0, 0],
    ["H", 0, 0, 0, 0, 0],
    ["I", 0, 0, 0, 0, 0],
    ["J", 0, 0, 0, 0, 0]
]

@app.route('/')
def home():
    return jsonify(message='Hello from the backend!')

@app.route('/getNewTileGrid')
def getNewTileGrid():
    return jsonify({'tileGrid': tileGrid_data})

if __name__ == '__main__':
    app.run(debug=True)