from betterchess.core.user import User
from betterchess.data_manager.base_manager import BaseDataManager
from betterchess.utils.config import Config
from betterchess.utils.handlers import EnvHandler, FileHandler, InputHandler, RunHandler

if __name__ == "__main__":
    env_handler = EnvHandler()
    run_type = input(
        "Do you want to run analysis or manage the database (run, manage): "
    )
    config = Config()
    config.create_config()
    input_handler = InputHandler()
    input_handler.collect_user_inputs()
    dbm = BaseDataManager(
        env_handler=env_handler, config=config, input_handler=input_handler
    )
    if run_type == "manage":
        dbm.select_manager()
    else:
        file_handler = FileHandler(input_handler.username)
        run_handler = RunHandler(file_handler=file_handler)
        engine = run_handler.create_engine()
        logger = run_handler.create_logger()
        user = User(input_handler, file_handler, run_handler, env_handler)
        user.analyse()
        print("Finished user analysis")
