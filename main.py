import mysql.connector
from sqlalchemy import create_engine

from betterchess.core.user import User
from betterchess.data_manager.managers import DatabaseManager
from betterchess.utils.config import Config
from betterchess.utils.handlers import FileHandler, InputHandler, RunHandler

if __name__ == "__main__":
    run_type = input(
        "Do you want to run analysis or manage the database (run, manage): "
    )
    if run_type == "manage":
        conn = mysql.connector.connect(
            host="localhost", user="root", database="better_chess"
        )
        mysql_engine = create_engine("mysql://root@localhost:3306/better_chess")
        config = Config()
        dbm = DatabaseManager(
            config=config, database_path="./data/betterchess.db", conn=conn
        )
        dbm.query_selector()
    else:
        input_handler = InputHandler()
        user_inputs = input_handler.user_input_dict()
        file_handler = FileHandler(input_handler.username)
        run_handler = RunHandler(file_handler=file_handler)

        username = user_inputs["username"]
        edepth = user_inputs["edepth"]
        start_date = user_inputs["start_date"]
        engine = run_handler.create_engine()
        logger = run_handler.create_logger()

        user = User(input_handler, file_handler, run_handler)
        user.analyse()
