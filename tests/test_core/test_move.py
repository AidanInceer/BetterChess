import unittest
from unittest.mock import MagicMock, patch

import pytest

from betterchess.core.move import Move


def test_castling_type_bl():
    piece = "king"
    move_col = "black"
    str_ml = "e8c8"
    assert "black_long" == Move.castling_type(piece, move_col, str_ml)
