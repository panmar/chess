from os import environ
import psycopg
from psycopg import DatabaseError, sql
import json
import database.config as config

db_user = environ["DB_USER"]
db_password = environ["DB_PASSWORD"]
db_name = environ["DB_NAME"]
db_port = environ["DB_PORT"]
connection_info = f"host={config.host} port={config.port} dbname={config.name} user={config.user} password={config.password}"


def connect():
    return psycopg.connect(connection_info)


def try_init_board(room_id, board):
    with connect() as connection:
        query = f"""
            INSERT INTO BOARDS(room_uuid, board)
            VALUES(%s, %s)
            ON CONFLICT (room_uuid) DO NOTHING
        """
        connection.execute(sql.SQL(query), [room_id, json.dumps(board)])


def set_board(room_id, board):
    with connect() as connection:
        query = f"""
            INSERT INTO BOARDS(room_uuid, board)
            VALUES(%s, %s)
            ON CONFLICT (room_uuid) DO UPDATE
                SET room_uuid=excluded.room_uuid,
                    board=excluded.board
        """
        connection.execute(sql.SQL(query), [room_id, json.dumps(board)])


def get_board(room_id):
    with connect() as connection:
        query = f"""
            SELECT board FROM BOARDS
            WHERE room_uuid = %s
        """

        result = connection.execute(sql.SQL(query), [room_id]).fetchone()
        if result:
            return json.loads(result[0])
        return None


def join_player_with_color(connection, room, color):
    try:
        query = f"""
            INSERT INTO ROOMS(room, color)
            VALUES(%s, %s)
        """
        connection.execute(sql.SQL(query), [room, color])
    except DatabaseError:
        connection.rollback()
        return False
    else:
        connection.commit()
        return True


def join_player(room):
    with connect() as connection:
        colors = ["white", "black"]
        for color in colors:
            if join_player_with_color(connection, room, color):
                return color

        return "observer"
