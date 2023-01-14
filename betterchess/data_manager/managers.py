import os
import shutil
from dataclasses import dataclass

from mysql.connector import MySQLConnection
from sqlalchemy import create_engine

from betterchess.utils.config import Config


@dataclass
class DatabaseManager:
    config: Config
    database_path: str
    conn: MySQLConnection

    def query_selector(self):
        selection = input(
            "Choose from the following list of options (reset, info, size, head, pass): "
        )
        if selection.lower() == "reset":
            self.reset_database()
            self.reset_logs()
        elif selection.lower() == "info":
            self.view_table_info()
        elif selection.lower() == "size":
            self.view_table_size()
        elif selection.lower() == "head":
            self.select_head_all_tables()
        elif selection.lower() == "pass":
            pass
        else:
            print("Please choose a valid option")

    def reset_logs(self):
        folder = "./logs"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    def reset_database(self):

        curs = self.conn.cursor()
        queries = [
            self.config.config.drop_game_table.file_path,
            self.config.config.drop_move_table.file_path,
            self.config.config.drop_pgn_table.file_path,
            self.config.config.create_game_table.file_path,
            self.config.config.create_move_table.file_path,
            self.config.config.create_pgn_table.file_path,
        ]
        for query in queries:
            sql = self._get_sql_file(query)
            curs.execute(sql)
            self.conn.commit()
        self.conn.close()
        print("database reset")

    def view_table_info(self):
        curs = self.conn.cursor()
        curs.execute("""PRAGMA table_info(move_data)""")
        print(curs.fetchall())
        curs.execute("""PRAGMA table_info(game_data)""")
        print(curs.fetchall())
        curs.execute("""PRAGMA table_info(pgn_data)""")
        print(curs.fetchall())
        self.conn.close()

    def view_table_size(self):
        curs = self.conn.cursor()
        queries = [
            (self.config.config.select_game_data_all.file_path, "game_data rows"),
            (self.config.config.select_move_data_all.file_path, "move_data rows"),
            (self.config.config.select_pgn_data_all.file_path, "pgn_data rows"),
        ]
        for query, name in queries:
            sql = self._get_sql_file(query)
            curs.execute(sql)
            print(f"{name}: {len(curs.fetchall())}")
        self.conn.close()

    def select_head_all_tables(self):
        curs = self.conn.cursor()
        queries = [
            self.config.config.select_game_data.file_path,
            self.config.config.select_move_data.file_path,
            self.config.config.select_pgn_data.file_path,
        ]
        for query in queries:
            sql = self.get_sql_file(query)
            curs.execute(sql)
            rows = curs.fetchall()
            for row in rows:
                print(row)
            print("-------------------------------------------------")
        self.conn.close()

    def _get_sql_file(self, sqlfilepath):
        with open(sqlfilepath) as file:
            sql = file.read()
        return sql


if __name__ == "__main__":
    c = Config()
    dbm = DatabaseManager(c, database_path="./data/betterchess.db")
    dbm.query_selector()
