from multiprocessing import Process
import chess
import chess.engine
import chess.pgn
import os

from sympy import besseli
import move_funcs

global board

# Set up file path references
dirname = os.path.dirname(__file__)
stk_path = r"../lib/stockfish_14.1/stockfish_14.1_win_x64_avx2.exe"
file_temp = os.path.join(dirname, r"../data/temp.pgn")
file_stockfish = os.path.join(dirname, stk_path)

# Initialises Stockfish, sets engine depth
engine = chess.engine.SimpleEngine.popen_uci(file_stockfish)
edepth = 8

# Opens the pgn file, reads the pgn file and sets up the game
chess_game_pgn = open(file_temp)
chess_game = chess.pgn.read_game(chess_game_pgn)
board1 = chess_game.board()
board2 = chess_game.board()
move_num = 0


def best_move(board_var=board2):
    best_move = engine.play(board_var,
                            chess.engine.Limit(depth=edepth),
                            game=object())
    board_var.push_san(str(best_move.move))
    eval_bm_init = engine.analyse(board_var,
                                  chess.engine.Limit(depth=edepth),
                                  game=object())
    eval_bm = move_funcs.move_eval(eval_bm_init)
    str_bm = str(best_move.move)
    return str_bm, eval_bm


def mainline_move(move, board_var=board1):
    str_move = str(move)
    board_var.push_san(str_move)
    eval_ml_init = engine.analyse(board_var,
                                  chess.engine.Limit(depth=edepth),
                                  game=object())
    eval_ml = move_funcs.move_eval(eval_ml_init)
    return eval_ml


if __name__ == '__main__':
    for move in chess_game.mainline_moves():
        bm = Process(target=best_move())
        bm.start()
        ml = Process(target=mainline_move(move))
        ml.start()
        board2 = board1
        print(f"{move} {bm} {ml}")
