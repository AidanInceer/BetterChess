from dataclasses import dataclass

import mysql.connector
from mysql.connector import MySQLConnection

from betterchess.utils.config import Config

from .managers import MySQLManager, SQLiteManager


@dataclass
class BaseDataManager:
    db_type: str
    config: Config

    def select_manager(self):
        if self.db_type == "mysql":
            self.mysql_manager()
        if self.db_type == "sqlite":
            self.sqlite_manager()

    def mysql_manager(self):
        conn = mysql.connector.connect(
            host="localhost", user="root", database="better_chess"
        )
        mysql_manager = MySQLManager(self.config, conn)
        mysql_manager.query_selector()

    def sqlite_manager(self):
        database_path = "./data/betterchess.db"
        sqlite_manager = SQLiteManager(self.config, database_path)
        sqlite_manager.query_selector()
