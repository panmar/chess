import psycopg2
from psycopg2 import DatabaseError


def initialize(cursor):
    sql = """
        DROP TABLE IF EXISTS ROOMS;
        CREATE TABLE IF NOT EXISTS ROOMS (
            room INTEGER NOT NULL,
            color VARCHAR(10) NOT NULL,
            PRIMARY KEY (room, color)
        );
    """
    cursor.execute(sql)


def insert(cursor, room, color):
    sql = f"""
        INSERT INTO ROOMS(room, color)
        VALUES({room}, '{color}')
    """
    cursor.execute(sql)


def test():
    connection = psycopg2.connect(
        host="localhost",
        port=32768,
        database="postgres",
        user="postgres",
        password="postgrespw",
    )

    with connection.cursor() as cursor:
        try:
            initialize(cursor)
            insert(cursor, 1, "white")
            insert(cursor, 1, "black")
        except DatabaseError as error:
            print(f"Error: {error}")
        else:
            connection.commit()

        print("Test begins...")

        try:
            insert(cursor, 2, "black")
            print("black inserted")
            insert(cursor, 1, "black")
            print("black inserted")
        except DatabaseError as error:
            print(f"Error: {error}")
        else:
            connection.commit()


if __name__ == "__main__":
    test()
