import unittest
from unittest.mock import MagicMock, patch

from betterchess.core.game import Game
from betterchess.core.user import Cleandown, PrepareUsers, User


class TestAnalyse(unittest.TestCase):
    def setUp(self):
        self.input_handler = MagicMock()
        self.file_handler = MagicMock()
        self.run_handler = MagicMock()
        self.env_handler = MagicMock()
        self.itermeta_data = MagicMock()
        self.user = User(
            self.input_handler, self.file_handler, self.run_handler, self.env_handler
        )
        self.prepare_users = PrepareUsers()
        self.cleandown = Cleandown()
        self.game = Game(
            self.input_handler,
            self.file_handler,
            self.run_handler,
            self.env_handler,
            self.itermeta_data,
        )
        self.input_handler.username = "test_user"
        self.file_handler.path_userlogfile = "test_path"
        self.run_handler.logger = "test_logger"

    @patch("betterchess.utils.extract.Extract.run_data_extract")
    @patch("betterchess.core.user.User.run_analysis")
    def test_analyse(self, run_analysis_mock, run_data_extract_mock):
        self.user.analyse()
        run_data_extract_mock.assert_called_once()
        run_analysis_mock.assert_called_once()

    @patch("betterchess.core.game.Game.run_game_analysis")
    @patch("betterchess.core.user.PrepareUsers.current_game")
    @patch("betterchess.core.user.Cleandown.previous_run")
    @patch(
        "betterchess.core.user.PrepareUsers.current_run",
        return_value=({"game_data": [1, 2, 3, 4, 5]}, 5),
    )
    def test_run_analysis(self, mock_curr, mock_prev, mock_curr_game, mock_analysis):
        self.user.run_analysis()
        mock_curr.assert_called_once()
        mock_prev.assert_called_once()
        mock_curr_game.assert_called()
        mock_analysis.assert_called()


class TestPrepareUsers(unittest.TestCase):
    def setUp(self):
        self.path_database = "./database.db"
        self.username = "Ainceer"
        self.path_userlogfile = "./file.log"
        self.logger = MagicMock()
        self.env_handler = MagicMock()
        self.prepare_user = PrepareUsers()

    @patch("betterchess.core.user.PrepareUsers.init_game_logs")
    @patch(
        "betterchess.core.user.PrepareUsers.initialise_users_games",
        return_value=({"game_data": [1, 2, 3, 4, 5]}, 5),
    )
    def test_current_run(self, mock_init, mock_logs):
        self.prepare_user.current_run(
            self.path_database,
            self.username,
            self.path_userlogfile,
            self.logger,
            self.env_handler,
        )
        mock_init.assert_called_once()
        mock_logs.assert_called_once()
        assert self.prepare_user.current_run(
            self.path_database,
            self.username,
            self.path_userlogfile,
            self.logger,
            self.env_handler,
        ) == ({"game_data": [1, 2, 3, 4, 5]}, 5)

    @patch("betterchess.core.user.PrepareUsers.set_first_game_logdate")
    @patch("betterchess.core.user.PrepareUsers.numlines_in_logfile", return_value=0)
    def test_init_game_logs_zero(self, mock_log, mock_set):
        self.prepare_user.init_game_logs(
            self.username, self.path_userlogfile, self.logger
        )
        mock_log.assert_called_once()
        mock_set.assert_called_with(self.username, self.path_userlogfile, self.logger)

    @patch("betterchess.core.user.PrepareUsers.set_first_game_logdate")
    @patch("betterchess.core.user.PrepareUsers.numlines_in_logfile", return_value=1)
    def test_init_game_logs_non_zero(self, mock_log, mock_set):
        self.prepare_user.init_game_logs(
            self.username, self.path_userlogfile, self.logger
        )
        mock_log.assert_called_once()
        mock_set.assert_not_called()

    @patch("builtins.open", new_callable=MagicMock)
    def test_numlines_in_logfile(self, mock_open):
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.readlines.return_value = ["line1\n", "line2\n", "line3\n"]
        mock_check_logfile = MagicMock()
        self.prepare_user.check_logfile = mock_check_logfile
        self.assertEqual(
            self.prepare_user.numlines_in_logfile(self.path_userlogfile), 0
        )
        mock_open.assert_called_once_with(self.path_userlogfile, "r")
        mock_file.readlines.assert_called_once()

    @patch("builtins.open", new_callable=MagicMock)
    def test_set_first_game_logdate(self, mock_open):
        self.prepare_user.set_first_game_logdate(
            self.username, self.path_userlogfile, self.logger
        )
        mock_open.assert_called_once_with(self.path_userlogfile, mode="a")
        self.logger.info.assert_called_once_with("| Ainceer | 2020-01-01 00:00:00 | 0")

    def test_check_logfile(self):
        game_log_list = []
        lines = ["user", "user_analysis", "false"]
        self.prepare_user.check_logfile(game_log_list, lines)

        assert game_log_list == ["user", "user_analysis"]

    @patch("builtins.open")
    def test_current_game(self, mock_open):
        path_temp = "./temp.pgn"
        chess_game = MagicMock(return_value=";")
        self.prepare_user.current_game(path_temp, chess_game)
        mock_open.assert_called_once_with(path_temp, mode="w")


class TestCleandown(unittest.TestCase):
    def setUp(self):
        self.cleandown = Cleandown()
        self.path_userlogfile = "test_path"
        self.path_database = "/database.db"
        self.username = "test_user"
        self.env_handler = MagicMock()

    @patch("betterchess.core.user.Cleandown.clean_sql_table")
    @patch("betterchess.core.user.Cleandown.get_last_logged_game_num", return_value=3)
    def test_previous_run(self, mock_log, mock_clean):
        self.cleandown.previous_run(
            self.path_userlogfile, self.path_database, self.username, self.env_handler
        )
        mock_log.assert_called_once()
        mock_clean.assert_called_once()

    @patch(
        "betterchess.core.user.Cleandown.get_game_log_list",
        return_value=[
            "[INFO game] | Ainceer | 2020-11-09 16:02:24 | 5",
            "[INFO game] | Ainceer | 2020-11-09 16:27:24 | 6",
        ],
    )
    @patch("betterchess.core.user.Cleandown.logfile_not_empty", return_value=True)
    def test_get_last_logged_game_num(self, mock_logfile, mock_loglist):
        self.cleandown.get_last_logged_game_num(self.path_userlogfile)
        mock_logfile.assert_called_once()
        mock_loglist.assert_called_once()
        assert self.cleandown.get_last_logged_game_num(self.path_userlogfile) == 6

    @patch("builtins.open")
    def test_logfile_not_empty(self, mock_open):
        # arrange
        path_userlogfile = "userlogfile.txt"
        file_contents = "example file contents"
        mock_open.return_value.__enter__.return_value.readlines.return_value = (
            file_contents.splitlines()
        )

        result = self.cleandown.logfile_not_empty(path_userlogfile)

        # assert
        mock_open.assert_called_once_with(path_userlogfile, mode="r")
        self.assertTrue(result)

    @patch("builtins.open")
    def test_logfile_empty(self, mock_open):
        # arrange
        path_userlogfile = "userlogfile.txt"
        file_contents = ""
        mock_open.return_value.__enter__.return_value.readlines.return_value = (
            file_contents.splitlines()
        )
        # act
        result = self.cleandown.logfile_not_empty(path_userlogfile)
        # assert
        mock_open.assert_called_once_with(path_userlogfile, mode="r")
        self.assertFalse(result)

    def test_get_game_log_list(self):
        path_userlogfile = r"./tests/test_core/fixtures/test_log_list.txt"

        assert self.cleandown.get_game_log_list(path_userlogfile) == [
            "[INFO user] | Ainceer | 2020-01-01 00:00:00 | 0\n",
            "[INFO game] | Ainceer | 2020-11-08 22:00:49 | 0\n",
            "[INFO game] | Ainceer | 2020-11-08 23:10:17 | 1",
        ]

    def test_logfile_line_checker_multi(self):
        game_log_list = []
        lines = ["user", "user_analysis", "false"]
        self.cleandown.logfile_line_checker_multi(game_log_list, lines)
        assert game_log_list == ["user", "user_analysis"]
