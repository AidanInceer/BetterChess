import os
import unittest
import pandas as pd
from src import filter


class TestFilter(unittest.TestCase):
    def test_logfile_not_empty_true(self):
        logfilepath = "tests/test_files/test.log"
        assert filter.logfile_not_empty(logfilepath) is True

    def test_logfile_not_empty_false(self):
        logfilepath = "tests/test_files/test_empty.log"
        open(logfilepath, "x")
        assert filter.logfile_not_empty(logfilepath) is False
        os.remove(logfilepath)

    def test_logfile_line_checker_multi(self):
        log_list = []
        lines = ["1", "2", "3"]
        assert filter.logfile_line_checker_multi(log_list, lines) is None

    # def test_init_game_logs_pass(self):
    #     logfilepath = "tests/test_files/test.log"
    #     logger = logging.Logger("test")
    #     assert filter.init_game_logs(logfilepath, logger) is None

    # def test_init_game_logs_set(self):
    #     logfilepath = "tests/test_files/test2.log"
    #     logger = logging.Logger("test")
    #     assert filter.init_game_logs(logfilepath, logger) is None

    # def test_numlines_in_logfile(self):
    #     logfilepath = "tests/test_files/test.log"
    #     assert filter.numlines_in_logfile(logfilepath) == 3

    # def test_set_first_game_logdate(self):
    #     logfilepath = "tests/test_files/test.log"
    #     logger = logging.Logger("test")
    #     assert filter.set_first_game_logdate(logfilepath, logger) is None

    def test_logfile_line_checker_single(self):
        log_list = []
        lines = ["filter1", "filter2", "filter3"]
        assert filter.logfile_line_checker_single(log_list, lines) is None
