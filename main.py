import os

from dotenv import load_dotenv

from betterchess.core.user import User
from betterchess.data_manager.base_manager import BaseDataManager
from betterchess.utils.config import Config
from betterchess.utils.handlers import FileHandler, InputHandler, RunHandler

if __name__ == "__main__":
    load_dotenv()
    db_type = os.getenv("DB_TYPE")
    run_type = input(
        "Do you want to run analysis or manage the database (run, manage): "
    )
    config = Config()
    dbm = BaseDataManager(db_type=db_type, config=config)
    if run_type == "manage":
        dbm.select_manager()
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
