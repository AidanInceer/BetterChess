import os
import unittest
from src import filter
from unittest.mock import patch
import logging
import pandas as pd


class TestFilter(unittest.TestCase):
    def test_clean_movecsv(self):
        movefilepath = "tests/test_movefile.csv"
        logfilepath = "tests/test.log"
        open(movefilepath, "x")
        assert filter.clean_movecsv(movefilepath, logfilepath) is None
        os.remove(movefilepath)

    def test_file_exist_true(self):
        movefilepath = "tests/test_movefile.csv"
        open(movefilepath, "x")
        assert filter.file_exist(movefilepath) is True
        os.remove(movefilepath)

    def test_file_exist_false(self):
        movefilepath = "tests/test_movefile.csv"
        assert filter.file_exist(movefilepath) is False
        os.remove(movefilepath)

    def test_logfile_not_empty_true(self):
        logfilepath = "tests/test.log"
        assert filter.logfile_not_empty(logfilepath) is True

    def test_logfile_not_empty_false(self):
        logfilepath = "tests/test_empty.log"
        open(logfilepath, "x")
        assert filter.logfile_not_empty(logfilepath) is False
        os.remove(logfilepath)

    def test_logfile_line_checker_multi(self):
        log_list = []
        lines = ["1", "2", "3"]
        assert filter.logfile_line_checker_multi(log_list, lines) is None

    def test_clean_df(self):
        movefilepath = "tests/test_clean_df.csv"
        open(movefilepath, "x")
        llog_gamenum = 10
        unclean_df = pd.DataFrame({"Game_number": 10}, index=[0])
        assert filter.clean_df(movefilepath, unclean_df, llog_gamenum) is None
        os.remove(movefilepath)

    def test_init_game_logs_pass(self):
        logfilepath = "tests/test.log"
        logger = logging.Logger("test")
        assert filter.init_game_logs(logfilepath, logger) is None

    def test_init_game_logs_set(self):
        logfilepath = "tests/test2.log"
        logger = logging.Logger("test")
        assert filter.init_game_logs(logfilepath, logger) is None

    def test_numlines_in_logfile(self):
        logfilepath = "tests/test.log"
        assert filter.numlines_in_logfile(logfilepath) == 3

    def test_set_first_game_logdate(self):
        logfilepath = "tests/test.log"
        logger = logging.Logger("test")
        assert filter.set_first_game_logdate(logfilepath, logger) is None

    def test_logfile_line_checker_single(self):
        log_list = []
        lines = ["filter1", "filter2", "filter3"]
        assert filter.logfile_line_checker_single(log_list, lines) is None
