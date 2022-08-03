from betterchess.core.user import User
from betterchess.utils.handlers import InputHandler, FileHandler, RunHandler


if __name__ == "__main__":
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
