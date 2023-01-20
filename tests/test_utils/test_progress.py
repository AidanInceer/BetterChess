import unittest
from unittest.mock import MagicMock, patch

import pytest

from betterchess.utils.progress import Progress


class TestProgress:
    def test1(self):
        one = 1
        assert one == 1
