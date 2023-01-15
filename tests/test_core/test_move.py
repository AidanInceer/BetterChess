import unittest
from unittest.mock import MagicMock, patch

import chess
import pytest
from chess import WHITE
from chess.engine import Cp, Mate, PovScore

from betterchess.core.move import Move


def test_castling_type_bl():
    piece = "king"
    move_col = "black"
    str_ml = "e8c8"
    assert "black_long" == Move.castling_type(piece, move_col, str_ml)


def test_move_eval():
    move = {"score": PovScore(Cp(10), WHITE)}
    assert 10 == Move.move_eval(move)


def test_move_eval_mate():
    move = {"score": PovScore(Mate(-0), WHITE)}
    assert 0 == Move.move_eval(move)


def test_eval_delta_white():
    move_num, eval_bm, eval_ml = 2, 200, 20
    assert Move.eval_delta(move_num, eval_bm, eval_ml) == 180


def test_eval_delta_black():
    move_num, eval_bm, eval_ml = 3, 20, 20
    assert Move.eval_delta(move_num, eval_bm, eval_ml) == 0


def test_move_accuracy():
    ed = 100
    assert Move.move_accuracy(ed) == 87.5


def test_assign_move_type_p2():
    move_acc = 100
    assert Move.assign_move_type(move_acc) == 2


def test_assign_move_type_p1():
    move_acc = 99.7
    assert Move.assign_move_type(move_acc) == 1


def test_assign_move_type_p0():
    move_acc = 90
    assert Move.assign_move_type(move_acc) == 0


def test_assign_move_type_n1():
    move_acc = 60
    assert Move.assign_move_type(move_acc) == -1


def test_assign_move_type_n2():
    move_acc = 35
    assert Move.assign_move_type(move_acc) == -2


def test_assign_move_type_n3():
    move_acc = 20
    assert Move.assign_move_type(move_acc) == -3


def test_assign_move_type_n4():
    move_acc = 0
    assert Move.assign_move_type(move_acc) == -4


def test_get_piece_square_int():
    move = "a1a2"
    assert Move.get_piece_square_int(move) == 8


def test_chess_piece_pawn():
    curr_board = chess.BaseBoard()
    square_int = 8
    assert "pawn" == Move.chess_piece(curr_board, square_int)


def test_chess_piece_knight():
    curr_board = chess.BaseBoard()
    square_int = 1
    assert "knight" == Move.chess_piece(curr_board, square_int)


def test_chess_piece_bishop():
    curr_board = chess.BaseBoard()
    square_int = 2
    assert "bishop" == Move.chess_piece(curr_board, square_int)


def test_chess_piece_rook():
    curr_board = chess.BaseBoard()
    square_int = 0
    assert "rook" == Move.chess_piece(curr_board, square_int)


def test_chess_piece_queen():
    curr_board = chess.BaseBoard()
    square_int = 3
    assert "queen" == Move.chess_piece(curr_board, square_int)


def test_chess_piece_king():
    curr_board = chess.BaseBoard()
    square_int = 4
    assert "king" == Move.chess_piece(curr_board, square_int)


def test_chess_piece_none():
    curr_board = chess.BaseBoard()
    square_int = 32
    assert " " == Move.chess_piece(curr_board, square_int)


def test_move_colour_white():
    move_num = 2
    assert Move.move_colour(move_num) == "white"


def test_move_colour_black():
    move_num = 3
    assert Move.move_colour(move_num) == "black"


def test_castling_type_ws():
    piece = "king"
    move_col = "white"
    str_ml = "e1g1"
    assert "white_short" == Move.castling_type(piece, move_col, str_ml)


def test_castling_type_wl():
    piece = "king"
    move_col = "white"
    str_ml = "e1c1"
    assert "white_long" == Move.castling_type(piece, move_col, str_ml)


def test_castling_type_bs():
    piece = "king"
    move_col = "black"
    str_ml = "e8g8"
    assert "black_short" == Move.castling_type(piece, move_col, str_ml)


def test_castling_type_bl():
    piece = "king"
    move_col = "black"
    str_ml = "e8c8"
    assert "black_long" == Move.castling_type(piece, move_col, str_ml)


def test_castling_type_none():
    piece = "pawn"
    move_col = "white"
    str_ml = "e1g1"
    assert Move.castling_type(piece, move_col, str_ml) is None


def test_white_castle_move_num_y():
    castle_type = "white_short"
    move_num = 10
    assert Move.white_castle_move_num(castle_type, move_num) == 10


def test_white_castle_move_num_n():
    castle_type = None
    move_num = 10
    assert Move.white_castle_move_num(castle_type, move_num) == 0


def test_black_castle_move_num_y():
    castle_type = "black_short"
    move_num = 10
    assert Move.black_castle_move_num(castle_type, move_num) == 10


def test_black_castle_move_num_n():
    castle_type = None
    move_num = 10
    assert Move.black_castle_move_num(castle_type, move_num) == 0
