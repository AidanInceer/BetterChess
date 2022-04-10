import pandas as pd
import time
import chess
import chess.engine
import chess.pgn
import os
import move_funcs
import numba


# Set up file path references
dirname = os.path.dirname(__file__)
stk_path = r"../stockfish_14.1_win_x64_avx2/stockfish_14.1_win_x64_avx2.exe"
file_stockfish = os.path.join(dirname, stk_path)
file_logger = os.path.join(dirname, r"../docs/chess_game_logger.txt")
file_gd_pgn = os.path.join(dirname, r"../data/game_data_pgn.csv")
file_temp = os.path.join(dirname, r"../data/temp.pgn")
file_m_data = os.path.join(dirname, r"../data/move_data.csv")
file_g_data = os.path.join(dirname, r"../data/game_data.csv")


def get_user_data(username="Ainceer"):
    '''
    Main function to analyse chess games
    '''
    # Import/ update game data from csv
    game = pd.read_csv(file_temp)

    # Initialises Stockfish, sets engine depth
    engine = chess.engine.SimpleEngine.popen_uci(file_stockfish)
    edepth = 16

    # Opens the pgn file, reads the pgn file and sets up the game
    chess_game_pgn = open(file_temp)
    chess_game = chess.pgn.read_game(chess_game_pgn)
    board = chess_game.board()

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

        move_timer_2 = time.perf_counter()
        bm_t = bm_timer2-bm_timer1
        ml_t = ml_timer2-ml_timer1
        tot_t = move_timer_2-move_timer_1
        print(f"{move_num} B:{bm_t:0.4f} M:{ml_t:0.4f} T:{tot_t:0.4f}")


if __name__ == "__main__":
    get_user_data()
