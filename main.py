from betterchess.core.user import User
from betterchess.data_manager.base_manager import BaseDataManager
from betterchess.utils.config import Config
from betterchess.utils.handlers import EnvHandler, FileHandler, InputHandler, RunHandler

if __name__ == "__main__":

    env_handler = EnvHandler()
    db_type = env_handler.db_type
    run_type = input(
        "Do you want to run analysis or manage the database (run, manage): "
    )
    config = Config()
    dbm = BaseDataManager(db_type=db_type, config=config)
    if run_type == "manage":
        dbm.select_manager()
    else:
        input_handler = InputHandler()
        input_handler.collect_user_inputs()
        file_handler = FileHandler(input_handler.username)
        run_handler = RunHandler(file_handler=file_handler)

        engine = run_handler.create_engine()
        logger = run_handler.create_logger()

        user = User(input_handler, file_handler, run_handler, env_handler)
        user.analyse()
