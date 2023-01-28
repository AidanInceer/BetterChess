import json
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd

from betterchess.utils.extract import Extract


class TestExtract(unittest.TestCase):
    def setUp(self) -> None:
        self.input_handler = MagicMock()
        self.input_handler.username.return_value = "Ainceer"

        self.file_handler = MagicMock()
        self.file_handler.path_userlogfile.return_value = "./tests/test.log"

        self.run_handler = MagicMock()
        self.run_handler.logger.return_value = "logger"

        self.env_handler = MagicMock()
        self.env_handler.mysql_host = "test_host"
        self.env_handler.mysql_user = "test_user"
        self.env_handler.mysql_password = "test_password"
        self.env_handler.mysql_db = "test_db"
        self.env_handler.mysql_driver = "mysql"

        self.extract = Extract(
            self.input_handler, self.file_handler, self.run_handler, self.env_handler
        )

        self.urls = json.loads(
            '{"archives": ["https://example.com/pgn1", "https://example.com/pgn2"]}'
        )
        self.num_urls = len(self.urls["archives"])
        self.username_list = []
        self.url_date_list = []
        self.games_list = []
        self.pgn_df = pd.DataFrame(
            {
                "username": ["test_username"],
                "url_date": ["2022-12-01"],
                "game_data": ["test_game_data"],
            }
        )

    @patch("chessdotcom.get_player_game_archives")
    def test_run_data_extract(self, mock_get_player_game_archives):
        mock_logger = MagicMock()
        mock_urls = {
            "archives": [
                {
                    "url": "https://www.chess.com/games/archive/test1",
                    "date": "2022-01-01",
                },
                {
                    "url": "https://www.chess.com/games/archive/test2",
                    "date": "2022-01-02",
                },
            ]
        }
        mock_get_player_game_archives.return_value = MagicMock(json=mock_urls)
        mock_pgn_df = MagicMock()

        self.extract
        self.extract.get_data_from_urls = MagicMock(return_value=mock_pgn_df)
        self.extract.export_pgn_data = MagicMock()

        username = "testuser"
        path_userlogfile = "logs/testuser.log"
        self.extract.run_data_extract(username, path_userlogfile, mock_logger)

        mock_get_player_game_archives.assert_called_once_with(username)
        self.extract.get_data_from_urls.assert_called_once_with(
            mock_urls, 2, mock_logger, path_userlogfile, username, [], [], []
        )
        self.extract.export_pgn_data.assert_called_once_with(mock_pgn_df)

    def test_get_data_from_urls(self):
        # Arrange
        self.extract.in_curr_month = MagicMock(return_value=True)
        self.extract.url_in_log = MagicMock(return_value=False)
        self.extract.get_url_date = MagicMock(
            return_value=datetime.now().strftime("%Y-%m-%d")
        )
        self.extract.extract_filter = MagicMock(return_value=["game1", "game2"])
        self.extract.simple_progress_bar = MagicMock()

        # Act
        result = self.extract.get_data_from_urls(
            self.urls,
            self.num_urls,
            self.run_handler.logger,
            self.file_handler.path_userlogfile,
            self.input_handler.username,
            self.username_list,
            self.url_date_list,
            self.games_list,
        )

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 4)
        self.assertEqual(
            result["game_data"].tolist(), ["game1", "game2", "game1", "game2"]
        )
        self.extract.in_curr_month.assert_called()
        self.extract.url_in_log.assert_called()
        self.extract.get_url_date.assert_called()
        self.extract.extract_filter.assert_called()
        self.extract.simple_progress_bar.assert_called()

        self.env_handler = MagicMock()

    @patch("betterchess.utils.extract.Extract.collect_game_data")
    def test_extract_filter_no_logs(self, mock_collect_game_data):

        mock_collect_game_data.return_value = [1, 2, 3]

        result = self.extract.extract_filter("username", False, False, "url")
        self.assertEqual(result, [1, 2, 3])

    @patch("betterchess.utils.extract.Extract.filter_pgn_table")
    def test_extract_filter_logs_no_curr(self, mock_filter_pgn_table):
        mock_filter_pgn_table.return_value = None

        result = self.extract.extract_filter("username", True, False, "url")
        self.assertEqual(result, [])
        mock_filter_pgn_table.assert_not_called()

    @patch("betterchess.utils.extract.Extract.collect_game_data")
    @patch("betterchess.utils.extract.Extract.filter_pgn_table")
    def test_extract_filter_logs_curr(
        self, mock_filter_pgn_table, mock_collect_game_data
    ):
        mock_collect_game_data.return_value = [1, 2, 3]
        mock_filter_pgn_table.return_value = None

        result = self.extract.extract_filter("username", True, True, "url")
        self.assertEqual(result, [1, 2, 3])
        mock_filter_pgn_table.assert_called_once_with("username")

    @patch("requests.get")
    def test_collect_game_data(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            "games": [
                {"pgn": "1. e4 e5 2. Nf3 Nc6\n"},
                {"pgn": "1. d4 d5 2. c4 dxc4 3. e3 Nf6 4. Bxc4 e6"},
            ]
        }
        result = self.extract.collect_game_data("https://example.com/games")
        expected_result = [
            "1. e4 e5 2. Nf3 Nc6 ; ",
            "1. d4 d5 2. c4 dxc4 3. e3 Nf6 4. Bxc4 e6",
        ]
        self.assertEqual(result, expected_result)

    @patch(
        "betterchess.utils.extract.Extract.get_url_date",
        return_value=datetime(23, 1, 1, 0, 0, 0),
    )
    def test_url_in_log_true(self, mock_date):
        test_file_path = r"tests/test_utils/fixtures/test_url_in_log1.log"
        actual = self.extract.url_in_log(
            url="chess.com/testgame/date", path_userlogfile=test_file_path
        )
        assert actual is False

    @patch(
        "betterchess.utils.extract.Extract.get_url_date",
        return_value=datetime.strptime(
            "2023-01-01 00:00:00",
            "%Y-%m-%d %H:%M:%S",
        ),
    )
    def test_url_in_log_false(self, mock_date):
        test_file_path = r"tests/test_utils/fixtures/test_url_in_log2.log"
        actual = self.extract.url_in_log(
            url="chess.com/testgame/date", path_userlogfile=test_file_path
        )
        assert actual is True

    @patch("betterchess.utils.extract.Extract.get_curr_mth", return_value="2020-10-01")
    @patch("betterchess.utils.extract.Extract.get_url_date", return_value="2020-10-01")
    def test_in_curr_month_true(self, mock_gud, mock_gcm):
        url = r"url/2020-10-01"
        expected = True
        actual = self.extract.in_curr_month(url)
        mock_gud.assert_called()
        mock_gcm.assert_called()
        assert actual == expected

    @patch("betterchess.utils.extract.Extract.get_curr_mth", return_value="2020-11-01")
    @patch("betterchess.utils.extract.Extract.get_url_date", return_value="2020-10-01")
    def test_in_curr_month_false(self, mock_gud, mock_gcm):
        url = r"url/2020-10-01"
        expected = False
        actual = self.extract.in_curr_month(url)
        mock_gud.assert_called()
        mock_gcm.assert_called()
        assert actual == expected

    def test_get_curr_mth(self):
        yr = datetime.now().year
        mth = datetime.now().month
        day = 1
        expected = datetime(yr, mth, day)
        actual = self.extract.get_curr_mth()
        assert expected == actual

    def test_get_url_date(self):
        url = "https://api.chess.com/pub/player/ainceer/games/2020/11"
        url_date = datetime.strptime("2020-11-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        assert url_date == self.extract.get_url_date(url)

    def test_simple_progress_bar_t0(self):
        num = 1
        total = 100
        assert self.extract.simple_progress_bar(num, total) is None
