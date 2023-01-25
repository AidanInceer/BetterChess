import os
import unittest
from unittest.mock import MagicMock, mock_open, patch

from betterchess.data_manager.managers import MySQLManager, SQLiteManager


class TestMySQLManager(unittest.TestCase):
    def setUp(self):
        conn = MagicMock()
        config = MagicMock()
        input_handler = MagicMock()
        self.manager = MySQLManager(config, conn, input_handler)
        self.manager.view_table_size = MagicMock()
        self.manager.select_head_all_tables = MagicMock()
        self.manager.reset_database = MagicMock()
        self.manager.reset_logs = MagicMock()
        self.manager.conn.cursor = MagicMock()
        self.manager._get_sql_file = MagicMock(return_value="SQL")

    @patch("builtins.input", return_value="reset")
    def test_query_selector_reset(self, mock_input):
        self.manager.query_selector()
        self.manager.reset_database.assert_called_once()
        self.manager.reset_logs.assert_called_once()

    @patch("builtins.input", return_value="size")
    def test_query_selector_size(self, mock_input):
        self.manager.query_selector()
        self.manager.view_table_size.assert_called_once()

    @patch("builtins.input", return_value="head")
    def test_query_selector_head(self, mock_input):
        self.manager.query_selector()
        self.manager.select_head_all_tables.assert_called_once()

    def test_reset_logs(self):
        # Create a mock folder with a file and a directory
        conn = MagicMock()
        config = MagicMock()
        input_handler = MagicMock()
        manager = MySQLManager(config, conn, input_handler)
        folder = "./tests/test_data_manager/fixtures"
        test_file = "testuser"
        with patch("os.remove") as mock_remove:
            manager.reset_logs(folder, test_file)
            mock_remove.assert_called()

    @patch("builtins.print")
    def test_reset_database(self, mock_print):
        conn = MagicMock()
        config = MagicMock()
        input_handler = MagicMock()
        self.manager = MySQLManager(config, conn, input_handler)
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
        input_handler = MagicMock()
        self.manager = MySQLManager(config, conn, input_handler)
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
        input_handler = MagicMock()
        self.manager = MySQLManager(config, conn, input_handler)
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

    def test_get_sql_file(self):
        filepath = "./tests/test_data_manager/fixtures/test.sql"
        expected = "SQL"
        actual = self.manager._get_sql_file(filepath)
        print(actual)
        assert actual == expected


class TestSQLiteManager(unittest.TestCase):
    def setUp(self):
        conn = MagicMock()
        config = MagicMock()
        input_handler = MagicMock()
        self.manager = SQLiteManager(config, conn, input_handler)
        self.manager.view_table_size = MagicMock()
        self.manager.select_head_all_tables = MagicMock()
        self.manager.reset_database = MagicMock()
        self.manager.reset_logs = MagicMock()
        self.manager.conn.cursor = MagicMock()
        self.manager._get_sql_file = MagicMock(return_value="SQL")

    @patch("builtins.input", return_value="reset")
    def test_query_selector_reset(self, mock_input):

        self.manager.query_selector()
        self.manager.reset_database.assert_called_once()
        self.manager.reset_logs.assert_called_once()

    @patch("builtins.input", return_value="size")
    def test_query_selector_size(self, mock_input):
        self.manager.query_selector()
        self.manager.view_table_size.assert_called_once()

    @patch("builtins.input", return_value="head")
    def test_query_selector_head(self, mock_input):
        self.manager.query_selector()
        self.manager.select_head_all_tables.assert_called_once()

    def test_reset_logs(self):
        # Create a mock folder with a file and a directory
        conn = MagicMock()
        config = MagicMock()
        input_handler = MagicMock()
        manager = SQLiteManager(config, conn, input_handler)
        folder = "./tests/test_data_manager/fixtures"
        test_file = "testuser"
        with patch("os.remove") as mock_remove:
            manager.reset_logs(folder, test_file)
            mock_remove.assert_called()

    @patch("builtins.print")
    def test_reset_database(self, mock_print):
        conn = MagicMock()
        config = MagicMock()
        input_handler = MagicMock()
        self.manager = SQLiteManager(config, conn, input_handler)
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
        input_handler = MagicMock()
        self.manager = SQLiteManager(config, conn, input_handler)
        self.manager.conn.cursor = MagicMock()
        self.manager._get_sql_file = MagicMock(return_value="SQL")

        self.manager.conn.cursor().fetchall.return_value = [1, 2, 3]
        self.manager.view_table_size()
        self.manager.conn.cursor.assert_called()
        self.manager._get_sql_file.assert_called()
        self.manager.conn.close.assert_called()
        mock_print.assert_any_call("game_data rows: 3")
        mock_print.assert_any_call("move_data rows: 3")
        mock_print.assert_any_call("pgn_data rows: 3")

    @patch("builtins.print")
    def test_select_head_all_tables(self, mock_print):
        conn = MagicMock()
        config = MagicMock()
        input_handler = MagicMock()
        self.manager = SQLiteManager(config, conn, input_handler)
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
        self.manager.conn.close.assert_called()
        mock_print.assert_any_call([1, 2, 3])
        mock_print.assert_any_call([4, 5, 6])
        mock_print.assert_any_call([7, 8, 9])
        mock_print.assert_any_call("-------------------------------------------------")

    def test_get_sql_file(self):
        filepath = "./tests/test_data-manager/fixtures/test.sql"
        expected = "SQL"
        actual = self.manager._get_sql_file(filepath)
        assert actual == expected
