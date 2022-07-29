"""Main function for running analysis on a given chess.com user"""
from src.user_analysis import InputHandler
from src.user_analysis import FileHandler
from src.user_analysis import ChessUser


if __name__ == "__main__":
    input_handler = InputHandler.get_inputs()
    file_paths = FileHandler(input_handler["username"])
    user = ChessUser(
        input_handler["username"], input_handler["edepth"], input_handler["start_date"]
    )
    user.create_logger()
    user.create_engine()
    user.run_analysis()
    print("analysis completed")

