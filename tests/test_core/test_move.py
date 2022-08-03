from betterchess.core.move import Move
from unittest import TestCase

class TestMove(TestCase):
    def test_castling_type_bl(self):
        piece = "king"
        move_col = "black"
        str_ml = "e8c8"
        assert "black_long" == Move.castling_type(piece, move_col, str_ml)
