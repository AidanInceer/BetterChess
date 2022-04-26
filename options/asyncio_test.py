import asyncio
import chess
import chess.engine
import chess.pgn
import os
import file_funcs
import game_funcs
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


move_num = 0


async def main() -> None:
    transport, engine = await chess.engine.popen_uci(file_stockfish)
    chess_game_pgn = open(file_temp)
    chess_game = chess.pgn.read_game(chess_game_pgn)
    board = chess_game.board()
    for move in chess_game.mainline_moves():
        # determine best move eval
        best_move = await engine.play(board,
                                        chess.engine.Limit(depth=edepth),
                                        game=object())
        board.push(best_move.move)
        eval_bm_init = await engine.analyse(board,
                                            chess.engine.Limit(depth=edepth))
        eval_bm = move_funcs.move_eval(eval_bm_init)

        # Reset board
        board.pop()

        # Determine mainline move eval
        str_move = str(move)
        board.push_san(str_move)

        eval_ml_init = await engine.analyse(board,
                                            chess.engine.Limit(depth=edepth),
                                            game=object())
        eval_ml = move_funcs.move_eval(eval_ml_init)
    await engine.quit()

asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
asyncio.run(main())
