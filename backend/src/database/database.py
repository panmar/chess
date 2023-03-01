import psycopg2
from psycopg2 import DatabaseError

# SCHEMA

# ROOMS:
#   - id

# PAWN_TYPES*
#   - id
#   - type

# PAWN_COLORS*
#   - id
#   - color

# PAWNS
#   - room_id
#   - pawn_type_id
#   - position_x
#   - position_y
#   - pawn_color_id

# MOVES_HISTORY
#   - id
#   - room_id
#   - move_from
#   - move_to

# PLAYER_TYPES
#   - id
#   - pawn_colors_id [or NULL for observers]

# PLAYERS:
#   - id
#   - uuid
#   - room_id
#   - role: [white, black, observer]

def connect():
    connection = psycopg2.connect(
        host="localhost",
        port=32768,
        database="postgres",
        user="postgres",
        password="postgrespw",
    )

    return connection

def try_initialize(connection):
    def try_drop_table(name):
        sql = f"DROP TABLE IF EXISTS {name}"
        cursor.execute(sql)

    def try_create_table_pawn_types(cursor):
        sql = """
        CREATE TABLE IF NOT EXISTS PAWN_TYPES (
            id SERIAL PRIMARY KEY,
            type VARCHAR(10) NOT NULL
        );
        INSERT INTO PAWN_TYPES(type) VALUES('pawn');
        INSERT INTO PAWN_TYPES(type) VALUES('rock');
        INSERT INTO PAWN_TYPES(type) VALUES('knight');
        INSERT INTO PAWN_TYPES(type) VALUES('bishop');
        INSERT INTO PAWN_TYPES(type) VALUES('queen');
        INSERT INTO PAWN_TYPES(type) VALUES('king');
        """
        cursor.execute(sql)

    def try_create_table_pawn_colors(cursor):
        sql = """
        CREATE TABLE IF NOT EXISTS PAWN_COLORS (
            id SERIAL PRIMARY KEY,
            color VARCHAR(10) NOT NULL
        );
        INSERT INTO PAWN_COLORS(color) VALUES('white');
        INSERT INTO PAWN_COLORS(color) VALUES('black');        
        """
        cursor.execute(sql)


    with connection.cursor() as cursor:
        try:
            try_drop_table("PAWN_TYPES")
            try_drop_table("PAWN_COLORS")
            try_create_table_pawn_types(cursor)
            try_create_table_pawn_colors(cursor)
        except DatabaseError as error:
            print(error)
        else:
            connection.commit()






