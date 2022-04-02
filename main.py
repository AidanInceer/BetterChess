import pandas as pd
import chess
import chess.engine
import chess.pgn
import logging
from src import extract, game_funcs, move_funcs, misc_funcs
from datetime import datetime
import os

# Set up file path references
dirname = os.path.dirname(__file__)
file_stockfish = os.path.join(dirname, r"./stockfish_14.1_win_x64_avx2/stockfish_14.1_win_x64_avx2.exe")
file_logger = os.path.join(dirname, r"./docs/chess_game_logger.txt")
file_gd_pgn = os.path.join(dirname, r"./data/game_data_pgn.csv")
file_temp = os.path.join(dirname, r"./data/temp.pgn")
file_m_data = os.path.join(dirname, r"./data/move_data.csv")
file_g_data = os.path.join(dirname, r"./data/game_data.csv")

# Set up logging
logging.basicConfig(filename=file_logger,
                    format='[%(levelname)s %(module)s] %(asctime)s - %(message)s',
                    level=logging.INFO, datefmt='%Y/%m/%d %I:%M:%S')
logger = logging.getLogger(__name__)


def main(username="Ainceer"):
    '''
    Main function to analyse chess games
    '''
    # Import/ update game data from csv
    extract.data_extract(username)
    all_games_df = pd.read_csv(file_gd_pgn)
    game_num = 0
    total_games = len(all_games_df["game_data"])

    # Init logging file and collect last game date logged
    llogged_datetime = misc_funcs.rerun_filter()
    misc_funcs.clean_rerun_files()

    # Initialises Stockfish, sets engine depth
    engine = chess.engine.SimpleEngine.popen_uci(file_stockfish)
    edepth = 8

    for game in all_games_df["game_data"]:
        # Displays the number of games that have been analysed
        game_num += 1
        print(f"{game_num} / {total_games}")

        # Writes the temp pgn file from
        f = open(file_temp, "w")
        f.write(game)
        f.close()

        # Opens the pgn file, reads the pgn file and sets up the game
        chess_game_pgn = open(file_temp)
        chess_game = chess.pgn.read_game(chess_game_pgn)
        board = chess_game.board()

        # header and logfile checking
        game_date = chess_game.headers["UTCDate"]
        game_time = chess_game.headers["UTCTime"]
        game_date_time = f"{game_date} {game_time}"
        game_datetime = datetime.strptime(game_date_time, '%Y.%m.%d %H:%M:%S')

        # Run based analysis based on dates after last logged date
        if game_datetime >= llogged_datetime:

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

                # Determine best move and calculation
                best_move = engine.play(board, chess.engine.Limit(depth=edepth), game=object())
                board.push_san(str(best_move.move))
                eval_bm_init = engine.analyse(board, chess.engine.Limit(depth=edepth), game=object())
                eval_bm = move_funcs.move_eval(eval_bm_init)

                # Reset board
                board.pop()

                # Determine mainline move & calculation
                str_move = str(move)
                board.push_san(str_move)
                eval_ml_init = engine.analyse(board, chess.engine.Limit(depth=edepth), game=object())
                get_eval_mainline = move_funcs.move_eval(eval_ml_init)

                # Eval diff, move accuracy and type calculations
                move_eval_diff = move_funcs.eval_diff(move_num, eval_bm, get_eval_mainline)
                move_accuracy = move_funcs.move_acc(move_eval_diff)
                move_type = move_funcs.move_type(move_accuracy)

                # Append data to respective lists
                chess_game_move_num.append(move_num)
                chess_game_move.append(str_move)
                chess_game_best_move.append(best_move.move)
                chess_game_best_move_eval.append(eval_bm)
                chess_game_mainline_eval.append(get_eval_mainline)
                chess_game_move_eval_diff.append(move_eval_diff)
                chess_game_move_acc.append(move_accuracy)
                chess_game_move_type.append(move_type)

                # Move number iterator
                move_num += 1

                # Initialise DataFrame and export move_data
                df = pd.DataFrame({"Date": game_datetime,
                                   "Game_number": game_num,
                                   "edepth": edepth,
                                   "Game_date": game_date,
                                   "Move_number": move_num,
                                   "Move": str_move,
                                   "Best_move": best_move.move,
                                   "Move_eval": get_eval_mainline,
                                   "Best_move_eval": eval_bm,
                                   "Move_eval_diff": move_eval_diff,
                                   "Move accuracy": move_accuracy,
                                   "Move_type": move_type,
                                   }, index=[0])

                # copy move data to csv file
                df.to_csv(file_m_data, mode='a', header=False, index=False)

            logger.info(f"DateTime of last game entry |{game_datetime}|{game_num}")

            # Game accuracy calculations
            white_game_acc = game_funcs.game_acc_calc_white(chess_game_move_acc)
            black_game_acc = game_funcs.game_acc_calc_black(chess_game_move_acc)

            # Sum of move types white and black
            w_best, b_best, w_great, b_great, w_good, b_good, w_ok, b_ok, w_inaccuracy, b_inaccuracy, w_mistake, b_mistake, w_blunder, b_blunder = move_funcs.sum_move_type(chess_game_move_type)

            # Phase of game accuracy calculations
            ow, mw, ew, ob, mb, eb = game_funcs.game_phase_acc_calc(chess_game_move_acc)

            # Least accurate game section
            improvement_white = game_funcs.game_section_improvement_white(ow, mw, ew)
            improvement_black = game_funcs.game_section_improvement_black(ob, mb, eb)

            # Initialise DataFrame and export game data
            df2 = pd.DataFrame(
                {"Date": game_datetime,
                    "Game_number": game_num,
                    "edepth": edepth,
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
                    "No_blunder_user": w_blunder if username == "White" else b_blunder,
                    "Improvement_user": improvement_white if username == "White" else improvement_black,
                }, index=[0])

            # copy game data to csv file
            df2.to_csv(file_g_data, mode='a', header=False, index=False)

            # reset lists
            chess_game_best_move = []
            chess_game_move_num = []
            chess_game_move = []
            chess_game_mainline_eval = []
            chess_game_best_move_eval = []
            chess_game_move_eval_diff = []
            chess_game_move_acc = []
            chess_game_move_type = []

        # In game already in csv skip analysis
        else:
            pass


if __name__ == "__main__":
    main()
