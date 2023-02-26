from psycopg import DatabaseError
from psycopg_pool import ConnectionPool
import json
import atexit

connection_info = (
    "host=localhost port=32768 dbname=postgres user=postgres password=postgrespw"
)
pool = ConnectionPool(connection_info)


@atexit.register
def close_pool():
    pool.close()


def init():
    with pool.connection() as connection, connection.cursor() as cursor:
        try:
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
            cursor.execute(sql)
        except DatabaseError as e:
            print(e)
            connection.rollback()
        else:
            connection.commit()


init()


def try_init_board(room_id, board):
    with pool.connection() as connection, connection.cursor() as cursor:
        try:
            sql = f"""
                INSERT INTO BOARDS(room_uuid, board)
                VALUES('{room_id}', '{board}')
                ON CONFLICT (room_uuid) DO NOTHING
            """
            cursor.execute(sql)
        except DatabaseError as e:
            print(e)
            connection.rollback()
        else:
            connection.commit()


def set_board(room_id, board):
    with pool.connection() as connection, connection.cursor() as cursor:
        try:
            sql = f"""
                INSERT INTO BOARDS(room_uuid, board)
                VALUES('{room_id}', '{json.dumps(board)}')
                ON CONFLICT (room_uuid) DO UPDATE
                    SET room_uuid=excluded.room_uuid,
                        board=excluded.board
            """
            cursor.execute(sql)
        except DatabaseError as e:
            print(e)
            connection.rollback()
        else:
            connection.commit()


def get_board(room_id):
    with pool.connection() as connection, connection.cursor() as cursor:
        try:
            sql = f"""
                SELECT board FROM BOARDS
                WHERE room_uuid = '{room_id}'
            """
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return json.loads(result[0])
        except DatabaseError as e:
            print(e)
            connection.rollback()
        else:
            connection.commit()

    return None


def join_player_with_color(cursor, room, color):
    with pool.connection() as connection, connection.cursor() as cursor:
        try:
            sql = f"""
                INSERT INTO ROOMS(room, color)
                VALUES('{room}', '{color}')
            """
            cursor.execute(sql)
        except DatabaseError:
            connection.rollback()
            return False
        else:
            connection.commit()
            return True


def join_player(room):
    with pool.connection() as connection, connection.cursor() as cursor:
        colors = ["white", "black"]
        for color in colors:
            if join_player_with_color(cursor, room, color):
                return color

        return "observer"