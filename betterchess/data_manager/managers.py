import os
import shutil
from dataclasses import dataclass
from sqlite3 import Connection

from mysql.connector import MySQLConnection

from betterchess.utils.config import Config
from betterchess.utils.handlers import InputHandler


@dataclass
class MySQLManager:
    """Manager for the mysql database - allows the user to reset the databse & logs,
    select the head of all database tables and see the size of all the tables.

    Returns:
        None
    """

    config: Config
    conn: MySQLConnection
    input_handler: InputHandler

    def query_selector(self):
        """Selects the query which the user specifies."""
        selection = input(
            "Choose from the following list of options (reset, size, head): "
        )
        if selection.lower() == "reset":
            self.reset_database()
            self.reset_logs(folder="./logs", user=self.input_handler.username)
        elif selection.lower() == "size":
            self.view_table_size()
        elif selection.lower() == "head":
            self.select_head_all_tables()

    def reset_logs(self, folder: str, user: str):
        """Resets the logfile for the current user."""
        filename = rf"{user}.log"
        os.remove(f"{folder}/{filename}")

    def reset_database(self):
        """Resets the database - deletes all tables and recreates empty versions."""
        curs = self.conn.cursor()
        queries = [
            self.config.conf.mysql.drop_game_table.file_path,
            self.config.conf.mysql.drop_move_table.file_path,
            self.config.conf.mysql.drop_pgn_table.file_path,
            self.config.conf.mysql.create_game_table.file_path,
            self.config.conf.mysql.create_move_table.file_path,
            self.config.conf.mysql.create_pgn_table.file_path,
        ]
        for query in queries:
            sql = self._get_sql_file(query)
            curs.execute(sql)
            self.conn.commit()
        self.conn.close()
        print("atabase reset")

    def view_table_size(self):
        """Views all the tables and return the number of rows in each."""
        curs = self.conn.cursor()
        queries = [
            (self.config.conf.mysql.select_game_data_all.file_path, "game_data rows"),
            (self.config.conf.mysql.select_move_data_all.file_path, "move_data rows"),
            (self.config.conf.mysql.select_pgn_data_all.file_path, "pgn_data rows"),
        ]
        for query, name in queries:
            sql = self._get_sql_file(query)
            curs.execute(sql)
            print(f"{name}: {len(curs.fetchall())}")
        self.conn.close()

    def select_head_all_tables(self):
        """Select the head of all the tables."""
        curs = self.conn.cursor()
        queries = [
            self.config.conf.mysql.select_game_data.file_path,
            self.config.conf.mysql.select_move_data.file_path,
            self.config.conf.mysql.select_pgn_data.file_path,
        ]
        for query in queries:
            sql = self._get_sql_file(query)
            curs.execute(sql)
            rows = curs.fetchall()
            for row in rows:
                print(row)
            print("-------------------------------------------------")
        self.conn.close()

    def _get_sql_file(self, sqlfilepath: str):
        """Get an sql query for the specified filepath.

        Args:
            sqlfilepath (str): sqlfile path.

        Returns:
            sql (str): sql query
        """
        with open(sqlfilepath) as file:
            sql = file.read()
        return sql


@dataclass
class SQLiteManager:

    """Manager for the mysql database - allows the user to reset the databse & logs,
    select the head of all database tables and see the size of all the tables.

    Returns:
        None
    """

    config: Config
    conn: Connection
    input_handler: InputHandler

    def query_selector(self):
        """Selects the query which the user specifies."""
        selection = input(
            "Choose from the following list of options (reset, size, head): "
        )
        if selection.lower() == "reset":
            self.reset_database()
            self.reset_logs(folder="./logs", user=self.input_handler.username)
        elif selection.lower() == "size":
            self.view_table_size()
        elif selection.lower() == "head":
            self.select_head_all_tables()

    def reset_logs(self, folder: str, user: str):
        """Resets the logfile for the current user."""
        filename = rf"{user}.log"
        os.remove(f"{folder}/{filename}")

    def reset_database(self):
        """Resets the database - deletes all tables and recreates empty versions."""
        curs = self.conn.cursor()
        queries = [
            self.config.conf.sqlite.drop_game_table.file_path,
            self.config.conf.sqlite.drop_move_table.file_path,
            self.config.conf.sqlite.drop_pgn_table.file_path,
            self.config.conf.sqlite.create_game_table.file_path,
            self.config.conf.sqlite.create_move_table.file_path,
            self.config.conf.sqlite.create_pgn_table.file_path,
        ]
        for query in queries:
            sql = self._get_sql_file(query)
            curs.execute(sql)
            self.conn.commit()
        self.conn.close()
        print("database reset")

    def view_table_size(self):
        """Views all the tables and return the number of rows in each."""
        curs = self.conn.cursor()
        queries = [
            (
                self.config.conf.sqlite.select_game_data_all.file_path,
                "game_data rows",
            ),
            (
                self.config.conf.sqlite.select_move_data_all.file_path,
                "move_data rows",
            ),
            (self.config.conf.sqlite.select_pgn_data_all.file_path, "pgn_data rows"),
        ]
        for query, name in queries:
            sql = self._get_sql_file(query)
            curs.execute(sql)
            print(f"{name}: {len(curs.fetchall())}")
        self.conn.close()

    def select_head_all_tables(self):
        """Select the head of all the tables."""
        curs = self.conn.cursor()
        queries = [
            self.config.conf.sqlite.select_game_data.file_path,
            self.config.conf.sqlite.select_move_data.file_path,
            self.config.conf.sqlite.select_pgn_data.file_path,
        ]
        for query in queries:
            sql = self._get_sql_file(query)
            curs.execute(sql)
            rows = curs.fetchall()
            for row in rows:
                print(row)
            print("-------------------------------------------------")
        self.conn.close()

    def _get_sql_file(self, sqlfilepath):
        """Get an sql query for the specified filepath.

        Args:
            sqlfilepath (str): sqlfile path.

        Returns:
            sql (str): sql query
        """
        with open(sqlfilepath) as file:
            sql = file.read()
        return sql
