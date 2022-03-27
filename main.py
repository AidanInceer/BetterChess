import pandas as pd
import chess
import chess.engine
import chess.pgn
import functions
import extract
import logging
from datetime import datetime

logging.basicConfig(filename ="./chess_game_logger.txt", format='[%(levelname)s %(module)s] %(asctime)s - %(message)s', level = logging.INFO, datefmt='%Y/%m/%d %I:%M:%S')
logger = logging.getLogger(__name__)


def main(username="Ainceer"):
    '''
    Main function to analyse chess games
    '''

    # Update game csv
    extract.data_extract(username)

    # Import data from csv
    all_games_df = pd.read_csv(f".\data\game_data_pgn.csv")

    # Init logging file and collect last game date logged
    init_dt = datetime.strptime("2000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    logger.info(f"DateTime of last game entry |{init_dt}")
    llogged_datetime = functions.log_date_checker()

    # Initialises Stockfish, sets engine depth (Update the stockfish location if required)
    engine = chess.engine.SimpleEngine.popen_uci(
        r"C:\Users\Aidan\Desktop\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe")
    engine_depth = 1
    game_num = 0
    total_games = len(all_games_df["game_data"])

    for game in all_games_df["game_data"]:
        # Displays the number of games that have been analysed
        game_num += 1
        
        print(f"{game_num} / {total_games}")

        # Writes the temp pgn file from: get_game_data(), all_games, chess_game_string
        f = open(r"data\temp.pgn", "w")
        f.write(game)
        f.close()

        # Opens the pgn file, reads the pgn file and sets up the game
        chess_game_pgn = open(r"data\temp.pgn")
        chess_game = chess.pgn.read_game(chess_game_pgn)
        board = chess_game.board()

        # header and logfile checking
        game_date = chess_game.headers["UTCDate"]
        game_time = chess_game.headers["UTCTime"]
        game_date_time = f"{game_date} {game_time}"
        game_datetime = datetime.strptime(game_date_time, '%Y.%m.%d %H:%M:%S')
        print(game_datetime)

        # Sets up header output data
        chess_game_time_control = chess_game.headers["TimeControl"]
        white = chess_game.headers["White"]
        black = chess_game.headers["Black"]
        player = "White" if white == username else "Black"
        rating_white = chess_game.headers["WhiteElo"]
        rating_black = chess_game.headers["BlackElo"]
        my_rating = rating_white if player == "White" else rating_black
        if chess_game.headers["Result"] == "1-0":
            winner = "White"
        elif chess_game.headers["Result"] == "0-1":
            winner = "Black"
        else:
            winner = "Draw"

        # Initialises game output lists
        chess_game_best_move = []
        chess_game_move_num = []
        chess_game_move = []
        chess_game_mainline_eval = []
        chess_game_best_move_eval = []
        chess_game_move_eval_diff = []
        chess_game_move_acc = []
        chess_game_move_type = []

        move_num = 0
        # calculates move by move output data
        for move in chess_game.mainline_moves():
            # Determine best move
            best_move = engine.play(board, chess.engine.Limit(depth=engine_depth), game=object())
            board.push_san(str(best_move.move))

            # Best_move move and evaluation calculation
            get_eval_best_move_init = engine.analyse(board, chess.engine.Limit(depth=engine_depth), game=object())
            get_eval_best_move = functions.move_best_eval_calc(get_eval_best_move_init)

            # Reset board
            board.pop()

            # Determine mainline move
            str_move = str(move)

            # Mainline move and evaluation calculation
            board.push_san(str_move)
            get_eval_mainline_init = engine.analyse(board, chess.engine.Limit(depth=engine_depth), game=object())
            get_eval_mainline = functions.move_mainline_eval_calc(get_eval_mainline_init)

            # Calculation of eval diff
            move_eval_diff = functions.eval_diff(move_num, get_eval_best_move, get_eval_mainline)

            # Move accuracy and type calculations
            move_accuracy = functions.move_acc_func(move_eval_diff)
            move_type = functions.move_type_func(move_accuracy)

            # Append data to respective lists
            chess_game_move_num.append(move_num)
            chess_game_move.append(str_move)
            chess_game_best_move.append(best_move.move)
            chess_game_best_move_eval.append(get_eval_best_move)
            chess_game_mainline_eval.append(get_eval_mainline)
            chess_game_move_eval_diff.append(move_eval_diff)
            chess_game_move_acc.append(move_accuracy)
            chess_game_move_type.append(move_type)

            # Move number iterator
            move_num += 1

            # Initialise DataFrame and export move data
            df = pd.DataFrame({"Data_key": str(f"{game_num}, {game_date}, {engine_depth}"),
                               "Game_number": game_num,
                               "Engine_Depth": engine_depth,
                               "Game_date": game_date,
                               "Move_number": move_num,
                               "Move": str_move,
                               "Best_move": best_move.move,
                               "Move_eval": get_eval_mainline,
                               "Best_move_eval": get_eval_best_move,
                               "Move_eval_diff": move_eval_diff,
                               "Move accuracy": move_accuracy,
                               "Move_type": move_type,
                               }, index=[0])

            # copy move data to csv file
            df.to_csv(".\data\move_data.csv", mode='a', header=False)

        logger.info(f"DateTime of last game entry |{game_datetime}")

        # Game accuracy calculations
        white_game_acc = functions.game_acc_calc_white(chess_game_move_acc)
        black_game_acc = functions.game_acc_calc_black(chess_game_move_acc)

        # Sum of move types white and black
        w_best, b_best, w_great, b_great, w_good, b_good, w_ok, b_ok, w_inaccuracy, b_inaccuracy, w_mistake, b_mistake, w_blunder, b_blunder = functions.sum_move_type(chess_game_move_type)

        # Phase of game accuracy calculations
        ow, mw, ew, ob, mb, eb = functions.game_phase_acc_calc(chess_game_move_acc)

        # Least accurate game section
        improvement_white = functions.game_section_improvement_white(ow, mw, ew)
        improvement_black = functions.game_section_improvement_black(ob, mb, eb)

        # Initialise DataFrame and export game data
        df2 = pd.DataFrame({"Data_key": str(f"{username}, {engine_depth},{game_date}, {game_num}"),
                            "Game_number": game_num,
                            "Engine_Depth": engine_depth,
                            "Game_date": game_date,
                            "Game_type": chess_game_time_control,
                            "White_player": white,
                            "Black_player": black,
                            "White_rating": rating_white,
                            "Black_rating": rating_black,
                            "My_colour": username,
                            "My_rating": my_rating,
                            "Winner": winner,
                            "User_winner": True if username == winner else False,
                            "number_of_moves": move_num / 2,

                            "User_accuracy": white_game_acc if username == "White" else black_game_acc,
                            "User_opening_accuracy": ow if username == "White" else ob,
                            "User_middle_accuracy": mw if username == "White" else mb,
                            "User_end_accuracy": ew if username == "White" else eb,
                            "No_best_user": w_best if username == "White" else b_best,
                            "No_great_user": w_great if username == "White" else b_great,
                            "No_good_user": w_good if username == "White" else b_good,
                            "No_ok_user": w_ok if username == "White" else b_ok,
                            "No_inaccuracy_user": w_inaccuracy if username == "White" else b_inaccuracy,
                            "No_mistake_user": w_mistake if username == "White" else b_mistake,
                            "No_blunder_user": w_blunder if username == "White" else w_blunder,
                            "Improvement_user": improvement_white if username == "White" else improvement_black,
                            }, index=[0])

        # copy game data to csv file
        df2.to_csv(".\data\game_data.csv", mode='a', header=False)

        # reset lists
        chess_game_best_move = []
        chess_game_move_num = []
        chess_game_move = []
        chess_game_mainline_eval = []
        chess_game_best_move_eval = []
        chess_game_move_eval_diff = []
        chess_game_move_acc = []
        chess_game_move_type = []


if __name__ == "__main__":
    main()
