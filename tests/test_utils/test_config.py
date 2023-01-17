import unittest

from box import Box

from betterchess.utils.config import Config


class TestConfig(unittest.TestCase):
    def test_set_config_path(self):
        self.path = r"./config/datasets.yaml"
        assert Config.set_config_path(self) == self.path

    def test_create_config(self):
        path = r"./tests/test_utils/fixtures/test_config.yaml"
        test_config = Config(path)
        assert test_config.create_config() == {"data": Box({"a": 1, "b": 2})}
