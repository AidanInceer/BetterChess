import unittest
from unittest.mock import MagicMock, patch

import pytest

from betterchess.core.headers import Headers


class TestHeaders:
    def test1(self):
        one = 1
        assert one == 1
