import unittest
from unittest.mock import MagicMock, patch

import pytest

from betterchess.data_manager.managers import MySQLManager, SQLiteManager


class TestMySQLManager:
    def test1(self):
        one = 1
        assert one == 1


class TestSQLiteManager:
    def test1(self):
        one = 1
        assert one == 1
