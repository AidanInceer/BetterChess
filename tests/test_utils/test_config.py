import unittest
from unittest.mock import mock_open, patch

from betterchess.utils.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.path = r"./config/datasets.yaml"

    def test_set_config_path(self):
        assert Config.set_config_path(self) == self.path

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_create_config(self, mock_file):
        assert open(self.path).read() == "data"
