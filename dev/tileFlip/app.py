from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tileGrid_data = [
    [" ", "1\n1\n1\n", "3\n", "1\n3\n", "2\n", "4\n"],
    ["1\n1\n1\n", 0, 0, 0, 0, 0],
    ["1\n2\n", 0, 0, 0, 0, 0],
    ["5\n", 0, 0, 0, 0, 0],
    ["2\n1\n", 0, 0, 0, 0, 0],
    ["1\n1\n", 0, 0, 0, 0, 0]
]

@app.route('/')
def home():
    return jsonify(message='Hello from the backend!')

@app.route('/getNewTileGrid')
def getNewTileGrid():
    return jsonify({'tileGrid': tileGrid_data})

if __name__ == '__main__':
    app.run(debug=True)