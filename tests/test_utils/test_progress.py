import datetime
import unittest
from unittest.mock import patch

from betterchess.utils.progress import Progress

# class TestProgress(unittest.TestCase):
#     def test_progress_bar(self):
#         g = 1
#         t = 100
#         start_time = datetime(2020, 1, 1, 1, 1, 0)
#         end_time = datetime(2020, 1, 1, 1, 1, 30)
#         assert Progress.bar(g, t, start_time, end_time) is None

#     @patch("betterchess.utils.progress.timers")
#     def test_progress_bar_10hrs(self, mock_t):
#         mock_t.return_value = 3600
#         g = 1
#         t = 13
#         start_time = datetime(2020, 1, 1, 1, 1, 0)
#         end_time = datetime(2020, 1, 1, 1, 1, 30)
#         assert Progress.bar(g, t, start_time, end_time) is None

#     @patch("betterchess.utils.progress.timers")
#     def test_progress_bar_10mins(self, mock_t):
#         mock_t.return_value = 4800
#         g = 1
#         t = 13
#         start_time = datetime(2020, 1, 1, 1, 1, 0)
#         end_time = datetime(2020, 1, 1, 1, 1, 30)
#         assert Progress.bar(g, t, start_time, end_time) is None

#     def test_timer(self):
#         timer = 1
#         st = 1
#         et = 2
#         tl = []
#         assert timer == Progress.timers(st, et, tl)
