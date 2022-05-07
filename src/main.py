from chess_class_test import ChessUser
from chess_class_test import InputHandler


if __name__ == "__main__":
    input_handler = InputHandler.get_inputs()
    user = ChessUser(
        input_handler["username"],
        input_handler["edepth"],
        input_handler["start_date"]
    )
    user.create_logger()
    user.create_engine()
    user.run_analysis()
