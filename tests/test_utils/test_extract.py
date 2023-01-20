import unittest

from betterchess.utils.extract import Extract


class TestExtract(unittest.TestCase):
    def test_simple_progress_bar_t1(self):
        test_type = 1
        num = 1
        total = 100
        assert Extract.simple_progress_bar(num, total, test_type) is None
