import sqlite3
import os
from src.sql_querys import (
    DROP_MOVE_TABLE,
    DROP_GAME_TABLE,
    DROP_PGN_TABLE,
    CREATE_MOVE_TABLE,
    CREATE_GAME_TABLE,
    CREATE_PGN_TABLE,
    SELECT_GAME_DATA,
    SELECT_MOVE_DATA,
    SELECT_PGN_DATA,
    SELECT_MOVE_DATA_ALL,
    SELECT_GAME_DATA_ALL,
    SELECT_PGN_DATA_ALL,
)


class FileHandler:
    """Storage location for the data/lib/log filepaths."""

    def __init__(self):
        self.dir = os.path.dirname(__file__)
        self.db_location = "./data/betterchess.db"
        self.log_path = r"./logs/logs.log"


def reset_db():
    conn = sqlite3.connect(FileHandler().db_location)
    curs = conn.cursor()
    curs.execute(DROP_MOVE_TABLE)
    curs.execute(DROP_GAME_TABLE)
    curs.execute(DROP_PGN_TABLE)
    curs.execute(CREATE_MOVE_TABLE)
    curs.execute(CREATE_GAME_TABLE)
    curs.execute(CREATE_PGN_TABLE)
    conn.commit()
    conn.close()


def view_table_column_info():
    conn = sqlite3.connect(FileHandler().db_location)
    curs = conn.cursor()
    curs.execute("""PRAGMA table_info(move_data)""")
    print(curs.fetchall())
    curs.execute("""PRAGMA table_info(game_data)""")
    print(curs.fetchall())
    conn.close()


def view_table_size():
    conn = sqlite3.connect(FileHandler().db_location)
    curs = conn.cursor()
    curs.execute(SELECT_MOVE_DATA_ALL)
    move_rows = curs.fetchall()
    print(f"move_data rows: {len(move_rows)}")
    curs.execute(SELECT_GAME_DATA_ALL)
    game_rows = curs.fetchall()
    print(f"game_rows rows: {len(game_rows)}")
    curs.execute(SELECT_PGN_DATA_ALL)
    pgn_rows = curs.fetchall()
    print(f"pgn_rows rows: {len(pgn_rows)}")
    conn.close()


def view_db_tables():
    conn = sqlite3.connect(FileHandler().db_location)
    curs = conn.cursor()
    curs.execute(SELECT_MOVE_DATA)
    rows = curs.fetchall()
    for row in rows:
        print(row)
    print("-------------------------------------------------")
    curs.execute(SELECT_GAME_DATA)
    rows = curs.fetchall()
    for row in rows:
        print(row)
    conn.close()
    print("-------------------------------------------------")
    curs.execute(SELECT_PGN_DATA)
    rows = curs.fetchall()
    for row in rows:
        print(row)
    conn.close()


def view_move_table():
    conn = sqlite3.connect(FileHandler().db_location)
    curs = conn.cursor()
    curs.execute(SELECT_MOVE_DATA_ALL)
    move_rows = curs.fetchall()
    for row in move_rows:
        print(row)


def view_game_table():
    conn = sqlite3.connect(FileHandler().db_location)
    curs = conn.cursor()
    curs.execute(SELECT_GAME_DATA_ALL)
    move_rows = curs.fetchall()
    for row in move_rows:
        print(row)


def view_pgn_table():
    conn = sqlite3.connect(FileHandler().db_location)
    curs = conn.cursor()
    curs.execute(SELECT_PGN_DATA_ALL)
    move_rows = curs.fetchall()
    for row in move_rows:
        print(row)


if __name__ == "__main__":
    print("=================================================")
    x = str.upper(
        input(
            "R = RESET, S = SELECT ALL TABLES, I = TABLE COLUMN INFO, X = TABLE SIZE, VM = VIEW MOVE FULL TABLE, VG = VIEW MOVE FULL TABLE, VP: VIEW FULL PGN DATA: "
        )
    )
    if x == ("R"):
        print("Resetting Database")
        reset_db()
        print("Database Reset Successfully")
        print("=================================================")
    elif x == ("S"):
        view_db_tables()
        print("=================================================")
    elif x == ("I"):
        view_table_column_info()
        print("=================================================")
    elif x == ("X"):
        view_table_size()
        print("=================================================")
    elif x == ("VM"):
        view_move_table()
        print("=================================================")
    elif x == ("VG"):
        view_game_table()
        print("=================================================")
    elif x == ("VP"):
        view_pgn_table()
        print("=================================================")
    else:
        pass
