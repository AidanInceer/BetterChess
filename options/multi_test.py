from multiprocessing import Process
import chess
import chess.engine
import chess.pgn
import os
import move_funcs


# Set up file path references
dirname = os.path.dirname(__file__)
stk_path = r"../lib/stockfish_14.1/stockfish_14.1_win_x64_avx2.exe"
file_temp = os.path.join(dirname, r"../data/temp.pgn")
file_stockfish = os.path.join(dirname, stk_path)

# Initialises Stockfish, sets engine depth
engine = chess.engine.SimpleEngine.popen_uci(file_stockfish)
edepth = 16

# Opens the pgn file, reads the pgn file and sets up the game
chess_game_pgn = open(file_temp)
chess_game = chess.pgn.read_game(chess_game_pgn)
board = chess_game.board()
move_num = 0


def best_move(board_var):
    best_move = engine.play(board_var,
                            chess.engine.Limit(depth=edepth),
                            game=object())
    board_var.push_san(str(best_move.move))
    eval_bm_init = engine.analyse(board_var,
                                  chess.engine.Limit(depth=edepth),
                                  game=object())
    eval_bm = move_funcs.move_eval(eval_bm_init)
    str_bm = str(best_move.move)
    return str_bm, eval_bm, board_var


def mainline_move(move, board_var):
    str_move = str(move)
    board_var.push_san(str_move)
    eval_ml_init = engine.analyse(board_var,
                                  chess.engine.Limit(depth=edepth),
                                  game=object())
    eval_ml = move_funcs.move_eval(eval_ml_init)
    return eval_ml


if __name__ == '__main__':

    for i, move in enumerate(chess_game.mainline_moves()):
        fen = str(board.fen())
        ml = Process(target=(mainline_move), args=((move, board)))
        # bm = Process(target=(best_move), args=(chess.Board(fen),))

        print(ml)
        # print(bm)
        ml.start()
        # bm.start()

        ml.join()
        # bm.join()
