import pandas as pd
import time
import math
import chess
import chess.engine
import chess.pgn
import logging
import os
import function_file
import function_header
import function_game
import function_move
import extract
import parameters
import csv
from datetime import datetime


def get_user_data(username=parameters.username,
                  set_depth=parameters.engine_depth,
                  start_dt=parameters.start_datetime):
    '''This function analyses a users games and outputs move and game analysis
    to csv files.
    Args:
        username: specified username input.
        depth: Set the stockfish engine depth (1-22)
        start_dt: determine starting date to conduct analysis.
    Returns:
        game_data.csv: game data for a specific user.
        move_data.csv: move data for all games analysed for a specific user.
    '''
    # data file paths
    dirn = os.path.dirname(__file__)
    stk_path = r"../lib/stockfish_14.1/stockfish_14.1_win_x64_avx2.exe"
    file_stockfish = os.path.join(dirn, stk_path)
    file_logger = os.path.join(dirn, rf"../logs/{username}_game_log.txt")
    file_temp = os.path.join(dirn, r"../data/temp.pgn")
    file_m_data = os.path.join(dirn, r"../data/move_data.csv")
    file_g_data = os.path.join(dirn, r"../data/game_data.csv")
    file_pgn_data = os.path.join(dirn, rf"../data/pgn_data/{username}_pgn_data.csv")

    # Set up logging
    logging.basicConfig(filename=file_logger,
                        format='[%(levelname)s %(module)s] %(message)s',
                        level=logging.INFO, datefmt='%Y/%m/%d %I:%M:%S')
    logger = logging.getLogger(__name__)
    function_file.rerun_filter()
    llogged_datetime = function_file.rerun_filter()
    function_file.clean_rerun_files()

    # Import/ update game data from csv
    extract.data_extract(username)
    all_games_df = pd.read_csv(file_pgn_data)
    total_games = len(all_games_df["game_data"])
    game_num = 1

    # Initialises Stockfish, sets engine depth
    engine = chess.engine.SimpleEngine.popen_uci(file_stockfish)
    edepth = set_depth
    game_time_list = []

    for game_num, game in enumerate(all_games_df["game_data"]):
        # Reads game data from temp.pgn
        f = open(file_temp, "w")
        f.write(game)
        f.close()
        chess_game_pgn = open(file_temp)
        chess_game = chess.pgn.read_game(chess_game_pgn)
        board = chess_game.board()

        # Header data.
        game_date = chess_game.headers["UTCDate"]
        game_time = chess_game.headers["UTCTime"]
        game_date_time = f"{game_date} {game_time}"
        game_datetime = datetime.strptime(game_date_time, '%Y.%m.%d %H:%M:%S')

        # Run analysis based on dates after last logged date
        if (game_datetime >= llogged_datetime) and (game_datetime >= start_dt):
            analysis_time_s = time.perf_counter()

            # Header data.
            chess_game_time_control = chess_game.headers["TimeControl"]
            white = chess_game.headers["White"]
            black = chess_game.headers["Black"]
            player = "White" if white == username else "Black"
            rating_white = chess_game.headers["WhiteElo"]
            rating_black = chess_game.headers["BlackElo"]
            try:
                opening_class = chess_game.headers["ECO"]
            except KeyError:
                opening_class = "000"
            try:
                opening_name_raw = chess_game.headers["ECOUrl"]
            except KeyError:
                opening_name_raw = "/NA"
            opening_name = function_header.opening_clean(opening_name_raw)
            term_raw = chess_game.headers["Termination"]
            termination = function_header.termination_clean(term_raw, username)
            user_rating = rating_white if player == "White" else rating_black
            opp_rating = rating_black if player == "White" else rating_white
            if chess_game.headers["Result"] == "1-0":
                winner = "White"
            elif chess_game.headers["Result"] == "0-1":
                winner = "Black"
            else:
                winner = "Draw"
            if (winner == "White" and player == "White"):
                user_winner = True
            elif (winner == "Black" and player == "Black"):
                user_winner = True
            else:
                user_winner = False

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
                # Determine best move and calculation
                best_move = engine.play(board,
                                        chess.engine.Limit(depth=edepth),
                                        game=object())
                board.push_san(str(best_move.move))
                eval_bm_init = engine.analyse(board,
                                              chess.engine.Limit(depth=edepth),
                                              game=object())
                eval_bm = function_move.move_eval(eval_bm_init)

                # Reset board
                board.pop()

                # Determine mainline move & calculation
                str_move = str(move)
                board.push_san(str_move)
                eval_ml_init = engine.analyse(board,
                                              chess.engine.Limit(depth=edepth),
                                              game=object())
                eval_ml = function_move.move_eval(eval_ml_init)

                # Eval diff, move accuracy and type calculations
                mv_eval_diff = function_move.eval_diff(move_num, eval_bm, eval_ml)
                move_accuracy = function_move.move_acc(mv_eval_diff)
                move_type = function_move.move_type(move_accuracy)

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

                # Move data export
                df = pd.DataFrame({"Username": username,
                                   "Date": game_datetime,
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
                df.to_csv(file_m_data, mode='a', header=False, index=False)

            total_moves = math.ceil(move_num/2)

            # Game calculations
            w_gm_acc = function_game.w_accuracy(gm_mv_ac)
            b_gm_acc = function_game.b_accuracy(gm_mv_ac)
            w_best, b_best = function_move.sum_best_mv(move_type_list)
            w_great, b_great = function_move.sum_great_mv(move_type_list)
            w_good, b_good = function_move.sum_good_mv(move_type_list)
            w_ok, b_ok = function_move.sum_ok_mv(move_type_list)
            w_inac, b_inac = function_move.sum_inac_mv(move_type_list)
            w_mist, b_mist = function_move.sum_mist_mv(move_type_list)
            w_blndr, b_blndr = function_move.sum_blndr_mv(move_type_list)
            ow, mw, ew, ob, mb, eb = function_game.phase_accuracy(gm_mv_ac)
            impve_w = function_game.game_section_improvement_white(ow, mw, ew)
            impve_b = function_game.game_section_improvement_black(ob, mb, eb)

            # Game data export
            df2 = pd.DataFrame(
                {"Username": username,
                 "Date": game_datetime,
                 "Game_number": game_num,
                 "Engine_depth": edepth,
                 "Game_date": game_date,
                 "Game_type": chess_game_time_control,
                 "White_player": white,
                 "Black_player": black,
                 "White_rating": rating_white,
                 "Black_rating": rating_black,
                 "User_colour": player,
                 "User_rating": user_rating,
                 "opponent_rating": opp_rating,
                 "Winner": winner,
                 "User_winner": user_winner,
                 "Opening_name": opening_name,
                 "Opening_class": opening_class,
                 "Termination": termination,
                 "Number_of_moves": total_moves,
                 "Accuracy": w_gm_acc if username == white else b_gm_acc,
                 "Opening_accuracy": ow if username == white else ob,
                 "Mid_accuracy": mw if username == white else mb,
                 "End_accuracy": ew if username == white else eb,
                 "No_best": w_best if username == white else b_best,
                 "No_great": w_great if username == white else b_great,
                 "No_good": w_good if username == white else b_good,
                 "No_ok": w_ok if username == white else b_ok,
                 "No_inaccuracy": w_inac if username == white else b_inac,
                 "No_mistake": w_mist if username == white else b_mist,
                 "No_blunder": w_blndr if username == white else b_blndr,
                 "Improvement": impve_w if username == white else impve_b,
                 }, index=[0])
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

            analysis_time_e = time.perf_counter()
            analysis_time = analysis_time_e-analysis_time_s
            game_time_list.append(analysis_time)
            avg_game_time = sum(game_time_list)/len(game_time_list)
            time_r = ((total_games-game_num)*(avg_game_time))/3600
            hours_r = int(time_r)
            mins_r = (time_r - hours_r) * 60
            if hours_r == 1:
                print((f"| {game_num} / {total_games} | Estimated Time"
                       f" Remaining: {hours_r} Hour,  {mins_r:.1f} Mins"
                       f" | Analysis time: {analysis_time:.1f}s"))
            else:
                print((f"| {game_num} / {total_games} | Estimated Time"
                       f" Remaining: {hours_r} Hours,  {mins_r:.1f} Mins"
                       f" | Analysis time: {analysis_time:.1f}s"))
        # If game already in csv skip analysis
        else:
            pass

    game_time_list = []

    # Add column headers for the csv files.
    game_data = pd.read_csv(file_g_data, header=None)
    game_header_list = ["Username", "Date", "Game_number", "Engine_depth",
                        "Game_date", "Game_type", "White_player",
                        "Black_player", "White_rating", "Black_rating",
                        "User_colour", "User_rating", "opponent_rating",
                        "Winner", "User_winner", "Opening_name",
                        "Opening_class", "Termination", "Number_of_moves",
                        "Accuracy", "Opening_accuracy", "Mid_accuracy",
                        "End_accuracy", "No_best", "No_great", "No_good",
                        "No_ok", "No_inaccuracy", "No_mistake",
                        "No_blunder", "Improvement"]
    if "Username" in game_data:
        game_data.to_csv(file_g_data, header=False, index=False)
    else:
        game_data.to_csv(file_g_data, header=game_header_list, index=False)

    move_data = pd.read_csv(file_m_data, header=None)
    move_header_list = ["Username", "Date", "Game_number", "edepth",
                        "Game_date", "Move_number", "Move",
                        "Best_move", "Move_eval", "Best_move_eval",
                        "Move_eval_diff", "Move accuracy", "Move_type"]
    if "Username" in move_data:
        move_data.to_csv(file_m_data, header=False, index=False)
    else:
        move_data.to_csv(file_m_data, header=move_header_list, index=False)

    # Complete statement
    print(f"User: {username} data extract and analysis complete")


if __name__ == "__main__":
    get_user_data()
