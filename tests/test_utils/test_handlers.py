import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

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


class TestFileHandler:
    def test1(self):
        one = 1
        assert one == 1


class TestRunHandler:
    def test1(self):
        one = 1
        assert one == 1


class TestEnvHandler:
    def test1(self):
        one = 1
        assert one == 1
