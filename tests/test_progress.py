import unittest
from datetime import datetime
from src import progress
from unittest.mock import patch


class TestProgress(unittest.TestCase):
    @patch("src.progress.timers")
    def test_progress_bar(self, mock_t):
        mock_t.return_value = 1
        g = 1
        t = 100
        start_time = datetime(2020, 1, 1, 1, 1, 0)
        end_time = datetime(2020, 1, 1, 1, 1, 30)
        assert progress.progress_bar(g, t, start_time, end_time) == None

    @patch("src.progress.timers")
    def test_progress_bar_10hrs(self, mock_t):
        mock_t.return_value = 3600
        g = 1
        t = 13
        start_time = datetime(2020, 1, 1, 1, 1, 0)
        end_time = datetime(2020, 1, 1, 1, 1, 30)
        assert progress.progress_bar(g, t, start_time, end_time) == None

    @patch("src.progress.timers")
    def test_progress_bar_10mins(self, mock_t):
        mock_t.return_value = 4800
        g = 1
        t = 13
        start_time = datetime(2020, 1, 1, 1, 1, 0)
        end_time = datetime(2020, 1, 1, 1, 1, 30)
        assert progress.progress_bar(g, t, start_time, end_time) == None

    def test_timer(self):
        timer = 1
        st = 1
        et = 2
        tl = []
        assert timer == progress.timers(st, et, tl)
