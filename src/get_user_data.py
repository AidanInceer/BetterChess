import pandas as pd
import time
import chess
import chess.engine
import chess.pgn
import logging
import os
import extract
import file_funcs
import game_funcs
import move_funcs
from datetime import datetime

# Set up file path references
dirname = os.path.dirname(__file__)
stk_path = r"../stockfish_14.1_win_x64_avx2/stockfish_14.1_win_x64_avx2.exe"
file_stockfish = os.path.join(dirname, stk_path)
file_logger = os.path.join(dirname, r"../docs/chess_game_logger.txt")
file_gd_pgn = os.path.join(dirname, r"../data/game_data_pgn.csv")
file_temp = os.path.join(dirname, r"../data/temp.pgn")
file_m_data = os.path.join(dirname, r"../data/move_data.csv")
file_g_data = os.path.join(dirname, r"../data/game_data.csv")

# Set up logging
logging.basicConfig(filename=file_logger,
                    format='[%(levelname)s %(module)s] %(message)s',
                    level=logging.INFO, datefmt='%Y/%m/%d %I:%M:%S')
logger = logging.getLogger(__name__)


def get_user_data(username="Ainceer"):
    '''
    Main function to analyse chess games
    '''
    # Import/ update game data from csv
    extract.data_extract(username)
    all_games_df = pd.read_csv(file_gd_pgn)
    total_games = len(all_games_df["game_data"])
    game_num = 0

    # Init logging file and collect last game date logged
    file_funcs.rerun_filter()
    llogged_datetime = file_funcs.rerun_filter()
    file_funcs.clean_rerun_files()

    # Initialises Stockfish, sets engine depth
    engine = chess.engine.SimpleEngine.popen_uci(file_stockfish)
    edepth = 16

    for game_num, game in enumerate(all_games_df["game_data"]):
        # Displays the number of games that have been analysed
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
            gm_best_mv = []
            gm_mv_num = []
            gm_mv = []
            mainline_eval = []
            best_move_eval = []
            move_eval_diff = []
            gm_mv_ac = []
            move_type_list = []

            move_num = 0
            # calculates move by move output data

            logger.info(f"Game info | {game_datetime} |{game_num}")
            for move in chess_game.mainline_moves():
                move_timer_1 = time.perf_counter()
                # Determine best move and calculation

                bm_timer1 = time.perf_counter()
                best_move = engine.play(board,
                                        chess.engine.Limit(depth=edepth),
                                        game=object())
                board.push_san(str(best_move.move))
                eval_bm_init = engine.analyse(board,
                                              chess.engine.Limit(depth=edepth),
                                              game=object())
                eval_bm = move_funcs.move_eval(eval_bm_init)
                bm_timer2 = time.perf_counter()

                ml_timer1 = time.perf_counter()
                # Reset board
                board.pop()
                # Determine mainline move & calculation
                str_move = str(move)
                board.push_san(str_move)
                eval_ml_init = engine.analyse(board,
                                              chess.engine.Limit(depth=edepth),
                                              game=object())
                eval_ml = move_funcs.move_eval(eval_ml_init)
                ml_timer2 = time.perf_counter()

                # Eval diff, move accuracy and type calculations
                mv_eval_diff = move_funcs.eval_diff(move_num, eval_bm, eval_ml)
                move_accuracy = move_funcs.move_acc(mv_eval_diff)
                move_type = move_funcs.move_type(move_accuracy)

                # Append data to respective lists
                gm_mv_num.append(move_num)
                gm_mv.append(str_move)
                gm_best_mv.append(best_move.move)
                best_move_eval.append(eval_bm)
                mainline_eval.append(eval_ml)
                move_eval_diff.append(mv_eval_diff)
                gm_mv_ac.append(move_accuracy)
                move_type_list.append(move_type)

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
                                   "Move_eval": eval_ml,
                                   "Best_move_eval": eval_bm,
                                   "Move_eval_diff": mv_eval_diff,
                                   "Move accuracy": move_accuracy,
                                   "Move_type": move_type,
                                   }, index=[0])

                # copy move data to csv file
                df.to_csv(file_m_data, mode='a', header=False, index=False)
                move_timer_2 = time.perf_counter()

                bm_t = bm_timer2-bm_timer1
                ml_t = ml_timer2-ml_timer1
                tot_t = move_timer_2-move_timer_1
                print(f"{move_num} B:{bm_t:0.4f} M:{ml_t:0.4f} T:{tot_t:0.4f}")

            # Game accuracy calculations
            w_gm_acc = game_funcs.w_accuracy(gm_mv_ac)
            b_gm_acc = game_funcs.b_accuracy(gm_mv_ac)

            # Sum of move types white and black
            w_best, b_best = move_funcs.sum_best_mv(move_type_list)
            w_great, b_great = move_funcs.sum_great_mv(move_type_list)
            w_good, b_good = move_funcs.sum_good_mv(move_type_list)
            w_ok, b_ok = move_funcs.sum_ok_mv(move_type_list)
            w_inac, b_inac = move_funcs.sum_inac_mv(move_type_list)
            w_mist, b_mist = move_funcs.sum_mist_mv(move_type_list)
            w_blndr, b_blndr = move_funcs.sum_blndr_mv(move_type_list)

            # Phase of game accuracy calculations
            ow, mw, ew, ob, mb, eb = game_funcs.phase_accuracy(gm_mv_ac)

            # Least accurate game section
            impve_w = game_funcs.game_section_improvement_white(ow, mw, ew)
            impve_b = game_funcs.game_section_improvement_black(ob, mb, eb)

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

                    "accuracy": w_gm_acc if username == "White" else b_gm_acc,
                    "pening_accuracy": ow if username == "White" else ob,
                    "mid_accuracy": mw if username == "White" else mb,
                    "end_accuracy": ew if username == "White" else eb,
                    "No_best": w_best if username == "White" else b_best,
                    "No_great": w_great if username == "White" else b_great,
                    "No_good": w_good if username == "White" else b_good,
                    "No_ok": w_ok if username == "White" else b_ok,
                    "No_inaccuracy": w_inac if username == "White" else b_inac,
                    "No_mistake": w_mist if username == "White" else b_mist,
                    "No_blunder": w_blndr if username == "White" else b_blndr,
                    "Improvement": impve_w if username == "White" else impve_b,
                 }, index=[0])

            # copy game data to csv file
            df2.to_csv(file_g_data, mode='a', header=False, index=False)

            # reset lists
            gm_best_mv = []
            gm_mv_num = []
            gm_mv = []
            mainline_eval = []
            best_move_eval = []
            move_eval_diff = []
            gm_mv_ac = []
            move_type_list = []

        # In game already in csv skip analysis
        else:
            pass


if __name__ == "__main__":
    get_user_data()
