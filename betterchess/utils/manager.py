import mysql.connector

con = mysql.connector.connect(host="localhost", user="root", database="testdatabase")


class DataBaseManager:
    config: Config

    def reset_db():
        conn = sqlite3.connect(FileHandler().path_database)
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
        conn = sqlite3.connect(FileHandler().path_database)
        curs = conn.cursor()
        curs.execute("""PRAGMA table_info(move_data)""")
        print(curs.fetchall())
        curs.execute("""PRAGMA table_info(game_data)""")
        print(curs.fetchall())
        conn.close()

    def view_table_size():
        conn = sqlite3.connect(FileHandler().path_database)
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
        conn = sqlite3.connect(FileHandler().path_database)
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
        conn = sqlite3.connect(FileHandler().path_database)
        curs = conn.cursor()
        curs.execute(SELECT_MOVE_DATA_ALL)
        move_rows = curs.fetchall()
        for row in move_rows:
            print(row)

    def view_game_table():
        conn = sqlite3.connect(FileHandler().path_database)
        curs = conn.cursor()
        curs.execute(SELECT_GAME_DATA_ALL)
        move_rows = curs.fetchall()
        for row in move_rows:
            print(row)

    def view_pgn_table():
        conn = sqlite3.connect(FileHandler().path_database)
        curs = conn.cursor()
        curs.execute(SELECT_PGN_DATA_ALL)
        move_rows = curs.fetchall()
        for row in move_rows:
            print(row)
