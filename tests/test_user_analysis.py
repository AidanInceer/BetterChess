from src.user_analysis import ChessGame, ChessMove
from unittest.mock import Mock



class TestUser():

    def test_user_1(self):
        assert 1 == 1

    def test_user_2(self):
        assert 1 == 1

    def test_user_3(self):
        assert 1 == 1


class TestGame():

    def test_game_1(self):
        assert 1 == 1

    def test_game_2(self):
        assert 1 == 1

    def test_game_3(self):
        assert 1 == 1


class TestMove():

    def test_eval_delta_white(self):
        move_num, eval_bm, eval_ml = 2, 200, 20
        assert ChessMove.eval_delta(
            self,
            move_num,
            eval_bm,
            eval_ml) == 180

    def test_eval_delta_black(self):
        move_num, eval_bm, eval_ml = 2, 20, 20
        assert ChessMove.eval_delta(
            self,
            move_num,
            eval_bm,
            eval_ml) == 0

    def test_move_accuracy(self):
        ed = 100
        assert ChessMove.move_accuracy(self, ed) == 87.5

    def test_assign_move_type_p2(self):
        move_acc = 100
        assert ChessMove.assign_move_type(self, move_acc) == 2

    def test_assign_move_type_p1(self):
        move_acc = 99.7
        assert ChessMove.assign_move_type(self, move_acc) == 1

    def test_assign_move_type_p0(self):
        move_acc = 90
        assert ChessMove.assign_move_type(self, move_acc) == 0

    def test_assign_move_type_n1(self):
        move_acc = 60
        assert ChessMove.assign_move_type(self, move_acc) == -1

    def test_assign_move_type_n2(self):
        move_acc = 35
        assert ChessMove.assign_move_type(self, move_acc) == -2

    def test_assign_move_type_n3(self):
        move_acc = 20
        assert ChessMove.assign_move_type(self, move_acc) == -3

    def test_assign_move_type_n4(self):
        move_acc = 0
        assert ChessMove.assign_move_type(self, move_acc) == -4

    def test_filter_timecont_header_interval(self):
        tc_white = "180+5"
        tc_black = "180+5"
        assert ChessMove.filter_timecont_header(
            self,
            tc_white,
            tc_black) == (180, 180, 5)

    def test_filter_timecont_header(self):
        tc_white = "100"
        tc_black = "100"
        assert ChessMove.filter_timecont_header(
            self,
            tc_white,
            tc_black) == (100, 100, 0)

    def test_get_piece_square_int(self):
        move = "a1a2"
        assert ChessMove.get_piece_square_int(self, move) == 8

    def test_chess_piece(self):
        # move = "e2e4"
        # assert ChessMove.chess_piece(self, move) == "pawn"
        pass
