import logging
import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import chess
import chess.engine
import pytest

from betterchess.utils.handlers import EnvHandler, FileHandler, InputHandler, RunHandler


class TestInputHandler(unittest.TestCase):
    def test_collect_user_inputs(self):
        # Create an instance of the InputHandler class
        input_handler = InputHandler()

        # Use the patch decorator to mock the input function
        with patch("builtins.input", side_effect=["test_user", "5", "2022", "12"]):
            input_handler.collect_user_inputs()

        # Assert that the correct values were stored in the instance variables
        self.assertEqual(input_handler.username, "test_user")
        self.assertEqual(input_handler.edepth, 5)
        self.assertEqual(input_handler.start_year, "2022")
        self.assertEqual(input_handler.start_month, "12")
        self.assertEqual(input_handler.start_date, datetime(2022, 12, 1))

    def test_user_input_dict(self):
        # Create an instance of the InputHandler class
        input_handler = InputHandler()

        # Call the user_input_dict method with test values
        input_handler.user_input_dict("test_user", 5, datetime(2022, 12, 1))

        # Assert that the correct values were stored in the instance variables
        self.assertEqual(input_handler.username, "test_user")
        self.assertEqual(input_handler.edepth, 5)
        self.assertEqual(input_handler.start_date, datetime(2022, 12, 1))


class TestFileHandler(unittest.TestCase):
    def test_file_paths(self):
        # Create an instance of the FileHandler class
        file_handler = FileHandler("test_user")

        # Assert that the correct values are stored in the instance variables
        self.assertEqual(file_handler.username, "test_user")
        self.assertEqual(file_handler.rpath_stockfish, "../../lib/stkfsh_15/stk_15.exe")
        self.assertEqual(file_handler.rpath_database, "../../data/betterchess.db")
        self.assertEqual(file_handler.rpath_temp, "../../data/temp.pgn")
        self.assertEqual(file_handler.rpath_config_path, "../../config/datasets.yaml")

        # Use the patch decorator to mock the os.path.join function


class TestRunHandler(unittest.TestCase):
    def test_create_logger(self):
        # Create an instance of the FileHandler class
        file_handler = FileHandler("test_user")

        # Create an instance of the RunHandler class
        run_handler = RunHandler(file_handler)

        # Use the patch decorator to mock the logging.basicConfig function
        with patch("logging.basicConfig") as mock_basic_config:
            run_handler.create_logger()

            # Assert that the basicConfig function was called with the correct parameters
            mock_basic_config.assert_called_with(
                filename=file_handler.path_userlogfile,
                format="[%(levelname)s %(module)s] %(message)s",
                level=logging.INFO,
                datefmt="%Y/%m/%d %I:%M:%S",
            )

    def test_create_engine(self):
        # Create an instance of the FileHandler class
        file_handler = FileHandler("test_user")

        # Create an instance of the RunHandler class
        run_handler = RunHandler(file_handler)

        # Use the patch decorator to mock the chess.engine.SimpleEngine.popen_uci method
        with patch("chess.engine.SimpleEngine.popen_uci") as mock_popen_uci:
            run_handler.create_engine()

            # Assert that the popen_uci method was called with the correct argument
            mock_popen_uci.assert_called_with(file_handler.path_stockfish)


class TestEnvHandler(unittest.TestCase):
    def test_create_environment(self):
        # Create an instance of the EnvHandler class
        env_handler = EnvHandler()

        # Use the patch decorator to mock the os.getenv function
        with patch(
            "os.getenv", side_effect=["sqlite", "sqlite3", None, None, None, None]
        ):
            env_handler.create_environment()

            # Assert that the correct values were stored in the instance variables
            self.assertEqual(env_handler.db_type, "sqlite")
            self.assertEqual(env_handler.mysql_driver, "sqlite3")
            self.assertIsNone(env_handler.mysql_user)
            self.assertIsNone(env_handler.mysql_password)
            self.assertIsNone(env_handler.mysql_host)
            self.assertIsNone(env_handler.mysql_db)
