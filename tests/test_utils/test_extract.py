import unittest
from unittest.mock import MagicMock, patch

import pytest

from betterchess.utils.extract import Extract


class TestExtract:
    def test1(self):
        one = 1
        assert one == 1
