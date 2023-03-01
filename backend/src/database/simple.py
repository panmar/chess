from os import environ
import psycopg
from psycopg import DatabaseError
import json

db_user = environ["DB_USER"]
db_password = environ["DB_PASSWORD"]
db_name = environ["DB_NAME"]
db_port = environ["DB_PORT"]
connection_info = (
    f"host=db port={db_port} dbname={db_name} user={db_user} password={db_password}"
)


def connect():
    return psycopg.connect(connection_info)


def create_db():
    with connect() as connection:
        sql = """
            DROP TABLE IF EXISTS BOARDS;
            CREATE TABLE IF NOT EXISTS BOARDS (
                room_uuid UUID PRIMARY KEY,
                board VARCHAR(250) NOT NULL
            );

            DROP TABLE IF EXISTS ROOMS;
            CREATE TABLE IF NOT EXISTS ROOMS (
                room UUID NOT NULL,
                color VARCHAR(10) NOT NULL,
                PRIMARY KEY (room, color)
            );
        """
        connection.execute(sql)


def try_init_board(room_id, board):
    with connect() as connection:
        sql = f"""
            INSERT INTO BOARDS(room_uuid, board)
            VALUES('{room_id}', '{board}')
            ON CONFLICT (room_uuid) DO NOTHING
        """
        connection.execute(sql)


def set_board(room_id, board):
    with connect() as connection:
        sql = f"""
            INSERT INTO BOARDS(room_uuid, board)
            VALUES('{room_id}', '{json.dumps(board)}')
            ON CONFLICT (room_uuid) DO UPDATE
                SET room_uuid=excluded.room_uuid,
                    board=excluded.board
        """
        connection.execute(sql)


def get_board(room_id):
    with connect() as connection:
        sql = f"""
            SELECT board FROM BOARDS
            WHERE room_uuid = '{room_id}'
        """

        result = connection.execute(sql).fetchone()
        if result:
            return json.loads(result[0])
        return None


def join_player_with_color(connection, room, color):
    try:
        sql = f"""
            INSERT INTO ROOMS(room, color)
            VALUES('{room}', '{color}')
        """
        connection.execute(sql)
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
