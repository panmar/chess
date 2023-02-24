from dataclasses import dataclass
from logging import DEBUG
from flask import Flask, make_response, jsonify, request, redirect, url_for
import uuid

app = Flask(__name__, static_folder="../chess-app/build/", static_url_path="")
app.logger.setLevel(DEBUG)


@dataclass
class Room:
    colors: list[str]
    board: list[int]

    def __init__(self):
        self.colors = []
        # fmt: off
        self.board = [
            0x20, 0x30, 0x40, 0x50, 0x60, 0x40, 0x30, 0x20,
            0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11,
            0x21, 0x31, 0x41, 0x51, 0x61, 0x41, 0x31, 0x21,
        ]
        # fmt: on

    def is_black(self, position):
        return (self.board[position] % 16) == 0

    def is_white(self, position):
        return not self.is_black(position)


rooms = {}


@app.route("/")
def index():
    room_id = str(uuid.uuid4())
    return redirect(url_for("room", room_id=room_id))


@app.route("/<uuid:room_id>")
def room(room_id):
    resp = make_response(app.send_static_file("index.html"))

    if room_id not in rooms:
        rooms[room_id] = Room()

    player_color = request.cookies.get("color")
    if player_color:
        return resp

    all_colors = ["white", "black"]
    available_colors = [c for c in all_colors if c not in rooms[room_id].colors]

    if not available_colors:
        return resp

    player_color = available_colors.pop()
    rooms[room_id].colors.append(player_color)
    resp.set_cookie("color", player_color, path=request.path)

    return resp


@app.route("/<uuid:room_id>/status")
def status(room_id):
    if room_id not in rooms:
        rooms[room_id] = Room()
    return jsonify(rooms[room_id].board)


@app.route("/<uuid:room_id>/move/<int:moveFrom>/<int:moveTo>", methods=["POST"])
def move(room_id, moveFrom, moveTo):
    color = request.cookies.get("color")
    room = rooms[room_id]

    if not color or color == "observer":
        return jsonify(room.board)

    if color == "white" and room.is_black(moveFrom):
        return jsonify(room.board)

    if color == "black" and room.is_white(moveFrom):
        return jsonify(room.board)

    if moveTo != moveFrom:
        room.board[moveTo] = room.board[moveFrom]
        room.board[moveFrom] = 0x00

    return jsonify(room.board)
