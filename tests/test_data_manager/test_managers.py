import os
import unittest
from unittest.mock import MagicMock, mock_open, patch

import pytest

from betterchess.data_manager.managers import MySQLManager, SQLiteManager


class TestMySQLManager(unittest.TestCase):
    @patch("builtins.input", return_value="reset")
    def test_query_selector_reset(self, mock_input):
        # Create a MySQLManager instance
        conn = MagicMock()
        config = MagicMock()
        manager = MySQLManager(config, conn)
        manager.reset_database = MagicMock()
        manager.reset_logs = MagicMock()

        # Call the query_selector method
        manager.query_selector()

        # Assert that the correct methods were called
        manager.reset_database.assert_called_once()
        manager.reset_logs.assert_called_once()

    @patch("builtins.input", return_value="size")
    def test_query_selector_size(self, mock_input):
        # Create a MySQLManager instance
        conn = MagicMock()
        config = MagicMock()
        manager = MySQLManager(config, conn)
        manager.view_table_size = MagicMock()
        manager.select_head_all_tables = MagicMock()
        manager.reset_database = MagicMock()
        manager.reset_logs = MagicMock()

        # Call the query_selector method
        manager.query_selector()

        # Assert that the correct methods were called
        manager.view_table_size.assert_called_once()
        manager.select_head_all_tables.assert_not_called()
        manager.reset_database.assert_not_called()
        manager.reset_logs.assert_not_called()

    @patch("builtins.input", return_value="head")
    def test_query_selector_head(self, mock_input):
        # Create a MySQLManager instance
        conn = MagicMock()
        config = MagicMock()
        manager = MySQLManager(config, conn)
        manager.select_head_all_tables = MagicMock()
        manager.view_table_size = MagicMock()
        manager.reset_database = MagicMock()
        manager.reset_logs = MagicMock()

        # Call the query_selector method
        manager.query_selector()

        # Assert that the correct methods were called
        manager.view_table_size.assert_not_called()
        manager.select_head_all_tables.assert_called_once()
        manager.reset_database.assert_not_called()
        manager.reset_logs.assert_not_called()

    @patch("os.listdir")
    @patch("os.path")
    @patch("shutil.rmtree")
    def test_reset_logs(self, mock_rmtree, mock_path, mock_listdir):
        # Create a MySQLManager instance
        conn = MagicMock()
        config = MagicMock()
        manager = MySQLManager(config, conn)

        # Set up mock return values for os.path and os.listdir
        mock_path.isfile.return_value = True
        mock_path.join.return_value = "./logs/test.log"
        mock_listdir.return_value = ["test.log"]

        # Call the reset_logs method
        manager.reset_logs()

    @patch("builtins.print")
    def test_reset_database(self, mock_print):
        conn = MagicMock()
        config = MagicMock()
        self.manager = MySQLManager(config, conn)
        self.manager.conn.cursor = MagicMock()
        self.manager._get_sql_file = MagicMock(return_value="SQL")

        self.manager.reset_database()
        self.manager.conn.cursor.assert_called()
        self.manager._get_sql_file.assert_called()
        self.manager.conn.commit.assert_called()
        self.manager.conn.close.assert_called()
        mock_print.assert_called_with("database reset")

    @patch("builtins.print")
    def test_view_table_size(self, mock_print):

        conn = MagicMock()
        config = MagicMock()
        self.manager = MySQLManager(config, conn)
        self.manager.conn.cursor = MagicMock()
        self.manager._get_sql_file = MagicMock(return_value="SQL")

        self.manager.conn.cursor().fetchall.return_value = [1, 2, 3]
        self.manager.view_table_size()
        self.manager.conn.cursor.assert_called()
        self.manager._get_sql_file.assert_called()
        self.manager.conn.commit.assert_not_called()
        self.manager.conn.close.assert_called()
        mock_print.assert_any_call("game_data rows: 3")
        mock_print.assert_any_call("move_data rows: 3")
        mock_print.assert_any_call("pgn_data rows: 3")

    @patch("builtins.print")
    def test_select_head_all_tables(self, mock_print):
        conn = MagicMock()
        config = MagicMock()
        self.manager = MySQLManager(config, conn)
        self.manager.conn.cursor = MagicMock()
        self.manager._get_sql_file = MagicMock(return_value="SQL")
        self.manager.conn.cursor().fetchall.return_value = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        self.manager.select_head_all_tables()
        self.manager.conn.cursor.assert_called()
        self.manager._get_sql_file.assert_called()
        self.manager.conn.commit.assert_not_called()
        self.manager.conn.close.assert_called()
        mock_print.assert_any_call([1, 2, 3])
        mock_print.assert_any_call([4, 5, 6])
        mock_print.assert_any_call([7, 8, 9])
        mock_print.assert_any_call("-------------------------------------------------")

    @patch("builtins.open", mock_open(read_data="SQL"))
    def test_get_sql_file(self):
        conn = MagicMock()
        config = MagicMock()
        self.manager = MySQLManager(config, conn)
        self.manager.conn.cursor = MagicMock()
        self.manager._get_sql_file = MagicMock(return_value="SQL")
        result = self.manager._get_sql_file("file.sql")
        self.assertEqual(result, "SQL")


class TestSQLiteManager:
    @patch("builtins.input", return_value="reset")
    def test_query_selector_reset(self, mock_input):
        # Create a MySQLManager instance
        conn = MagicMock()
        config = MagicMock()
        manager = SQLiteManager(config, conn)
        manager.reset_database = MagicMock()
        manager.reset_logs = MagicMock()

        # Call the query_selector method
        manager.query_selector()

        # Assert that the correct methods were called
        manager.reset_database.assert_called_once()
        manager.reset_logs.assert_called_once()

    @patch("builtins.input", return_value="size")
    def test_query_selector_size(self, mock_input):
        # Create a SQLiteManager instance
        conn = MagicMock()
        config = MagicMock()
        manager = SQLiteManager(config, conn)
        manager.view_table_size = MagicMock()
        manager.select_head_all_tables = MagicMock()
        manager.reset_database = MagicMock()
        manager.reset_logs = MagicMock()

        # Call the query_selector method
        manager.query_selector()

        # Assert that the correct methods were called
        manager.view_table_size.assert_called_once()
        manager.select_head_all_tables.assert_not_called()
        manager.reset_database.assert_not_called()
        manager.reset_logs.assert_not_called()

    @patch("builtins.input", return_value="head")
    def test_query_selector_head(self, mock_input):
        # Create a SQLiteManager instance
        conn = MagicMock()
        config = MagicMock()
        manager = SQLiteManager(config, conn)
        manager.select_head_all_tables = MagicMock()
        manager.view_table_size = MagicMock()
        manager.reset_database = MagicMock()
        manager.reset_logs = MagicMock()

        # Call the query_selector method
        manager.query_selector()

        # Assert that the correct methods were called
        manager.view_table_size.assert_not_called()
        manager.select_head_all_tables.assert_called_once()
        manager.reset_database.assert_not_called()
        manager.reset_logs.assert_not_called()

    @patch("os.listdir")
    @patch("os.path")
    @patch("shutil.rmtree")
    def test_reset_logs(self, mock_rmtree, mock_path, mock_listdir):
        # Create a SQLiteManager instance
        conn = MagicMock()
        config = MagicMock()
        manager = SQLiteManager(config, conn)

        # Set up mock return values for os.path and os.listdir
        mock_path.isfile.return_value = True
        mock_path.join.return_value = "./logs/test.log"
        mock_listdir.return_value = ["test.log"]

        # Call the reset_logs method
        manager.reset_logs()

    @patch("builtins.print")
    def test_reset_database(self, mock_print):
        conn = MagicMock()
        config = MagicMock()
        self.manager = SQLiteManager(config, conn)
        self.manager.conn.cursor = MagicMock()
        self.manager._get_sql_file = MagicMock(return_value="SQL")

        self.manager.reset_database()
        self.manager.conn.cursor.assert_called()
        self.manager._get_sql_file.assert_called()
        self.manager.conn.commit.assert_called()
        self.manager.conn.close.assert_called()
        mock_print.assert_called_with("database reset")

    @patch("builtins.print")
    def test_view_table_size(self, mock_print):

        conn = MagicMock()
        config = MagicMock()
        self.manager = SQLiteManager(config, conn)
        self.manager.conn.cursor = MagicMock()
        self.manager._get_sql_file = MagicMock(return_value="SQL")

        self.manager.conn.cursor().fetchall.return_value = [1, 2, 3]
        self.manager.view_table_size()
        self.manager.conn.cursor.assert_called()
        self.manager._get_sql_file.assert_called()
        self.manager.conn.commit.assert_not_called()
        self.manager.conn.close.assert_called()
        mock_print.assert_any_call("game_data rows: 3")
        mock_print.assert_any_call("move_data rows: 3")
        mock_print.assert_any_call("pgn_data rows: 3")

    @patch("builtins.print")
    def test_select_head_all_tables(self, mock_print):
        conn = MagicMock()
        config = MagicMock()
        self.manager = SQLiteManager(config, conn)
        self.manager.conn.cursor = MagicMock()
        self.manager._get_sql_file = MagicMock(return_value="SQL")
        self.manager.conn.cursor().fetchall.return_value = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        self.manager.select_head_all_tables()
        self.manager.conn.cursor.assert_called()
        self.manager._get_sql_file.assert_called()
        self.manager.conn.commit.assert_not_called()
        self.manager.conn.close.assert_called()
        mock_print.assert_any_call([1, 2, 3])
        mock_print.assert_any_call([4, 5, 6])
        mock_print.assert_any_call([7, 8, 9])
        mock_print.assert_any_call("-------------------------------------------------")

    # @patch("builtins.open", mock_open(read_data="SQL"))
    # def test_get_sql_file(self):
    #     conn = MagicMock()
    #     config = MagicMock()
    #     self.manager = SQLiteManager(config, conn)
    #     self.manager.conn.cursor = MagicMock()
    #     self.manager._get_sql_file = MagicMock(return_value="SQL")
    #     result = self.manager._get_sql_file("file.sql")
    #     self.assertEqual(result, "SQL")
