from flask import Flask
from flask import jsonify

app = Flask(__name__)

chessboard = [
    0x20, 0x30, 0x40, 0x50, 0x60, 0x40, 0x30, 0x20,
    0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x21, 0x31, 0x41, 0x51, 0x61, 0x41, 0x31, 0x21,
    0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11,
]

@app.route('/status')
def status():
    return jsonify(chessboard)

@app.route('/move/<int:moveFrom>/<int:moveTo>')
def move(moveFrom, moveTo):
    if moveTo != moveFrom:
        chessboard[moveTo] = chessboard[moveFrom]
        chessboard[moveFrom] = 0x00;

    return jsonify(chessboard)