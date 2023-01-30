import sqlite3
from dataclasses import dataclass

import mysql.connector

from betterchess.utils.config import Config
from betterchess.utils.handlers import EnvHandler, InputHandler

from .managers import MySQLManager, SQLiteManager


@dataclass
class BaseDataManager:
    """Base datamanager which faciliates the selection of the database - given the `.env`
    parameter `DB_TYPE`.
    """

    env_handler: EnvHandler
    config: Config
    input_handler: InputHandler

    def select_manager(self):
        """Selects the database manager for the current environment."""
        if self.env_handler.db_type == "mysql":
            self.mysql_manager()
        if self.env_handler.db_type == "sqlite":
            self.sqlite_manager()

    def mysql_manager(self):
        """Connects to the mysql database and allows a user to manager the database."""
        conn = mysql.connector.connect(
            host=self.env_handler.mysql_host,
            user=self.env_handler.mysql_user,
            database=self.env_handler.mysql_db,
            password=self.env_handler.mysql_password,
        )
        mysql_manager = MySQLManager(self.config, conn, self.input_handler)
        mysql_manager.query_selector()

    def sqlite_manager(self):
        """Connects to the sqlite3 database and allows a user to manager the database."""
        conn = sqlite3.connect(r"./data/betterchess.db")
        sqlite_manager = SQLiteManager(self.config, conn, self.input_handler)
        sqlite_manager.query_selector()
