import unittest
from unittest.mock import MagicMock, patch

import pytest

from betterchess.utils.handlers import EnvHandler, FileHandler, InputHandler, RunHandler


class TestInputHandler:
    def test1(self):
        one = 1
        assert one == 1


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
