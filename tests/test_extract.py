from src import extract
from datetime import datetime


def test_get_url_date():
    url = "https://api.chess.com/pub/player/ainceer/games/2020/11"
    url_date = datetime.strptime("2020-11-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    assert url_date == extract.get_url_date(url)


def test_get_curr_month():
    curmth = datetime.strptime("2022-05-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    assert curmth == extract.get_curr_mth()


def test_in_cur_mth_false():
    url = "https://api.chess.com/pub/player/ainceer/games/2021/11"
    assert extract.in_curr_month(url) is False


def test_in_cur_mth_true():
    url = "https://api.chess.com/pub/player/ainceer/games/2022/05"
    assert extract.in_curr_month(url) is True
