import unittest
from unittest.mock import MagicMock, patch

import pytest

from betterchess.data_manager.base_manager import BaseDataManager


class TestBaseDataManager:
    def test1(self):
        one = 1
        assert one == 1
