from chess_class_test import UserAnalysis
from chess_class_test import InputHandler


if __name__ == "__main__":
    input_handler = InputHandler.get_inputs()
    run = UserAnalysis(
        input_handler["username"],
        input_handler["edepth"],
        input_handler["start_date"]
    )
    print("test1")
    run.analyse()
