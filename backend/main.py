from flask import Flask, make_response, jsonify, request, redirect, url_for
import uuid
import database.simple as db


app = Flask(__name__, static_folder="build/", static_url_path="")

# fmt: off
starting_board = [
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


def is_position_black(board, position):
    return (board[position] % 16) == 0


def is_position_white(board, position):
    return not is_position_black(board, position)


@app.route("/")
def index():
    room_id = str(uuid.uuid4())
    return redirect(url_for("room", room_id=room_id))


@app.route("/<uuid:room_id>")
def room(room_id):
    resp = make_response(app.send_static_file("index.html"))

    db.try_init_board(room_id, starting_board)

    player_color = request.cookies.get("color")
    if player_color:
        return resp

    role = db.join_player(room_id)

    if role == "observer":
        return resp

    player_color = role
    resp.set_cookie("color", role, path=request.path)

    return resp


@app.route("/<uuid:room_id>/status")
def status(room_id):
    board = db.get_board(room_id)
    return jsonify(board)


@app.route("/<uuid:room_id>/move/<int:moveFrom>/<int:moveTo>", methods=["POST"])
def move(room_id, moveFrom, moveTo):
    color = request.cookies.get("color")
    board = db.get_board(room_id)

    if not color or (color == "observer"):
        return jsonify(board)

    if color == "white" and is_position_black(board, moveFrom):
        return jsonify(board)

    if color == "black" and is_position_white(board, moveFrom):
        return jsonify(board)

    if moveTo != moveFrom:
        board[moveTo] = board[moveFrom]
        board[moveFrom] = 0x00
        db.set_board(room_id, board)

    return jsonify(board)
