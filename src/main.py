"""Main function for running analysis on a given chess.com user"""
from user_analysis import ChessUser
from user_analysis import InputHandler
from user_analysis import FileHandler

if __name__ == "__main__":
    input_handler = InputHandler.get_inputs()
    file_paths = FileHandler(input_handler["username"])
    user = ChessUser(
        input_handler["username"],
        input_handler["edepth"],
        input_handler["start_date"])
    user.create_logger()
    user.create_engine()
    user.run_analysis()
