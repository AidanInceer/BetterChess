from src import extract
from datetime import datetime

def test_get_url_date():
    url = "https://api.chess.com/pub/player/ainceer/games/2020/11"
    url_date = datetime.strptime("2020-11-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    assert url_date == extract.get_url_date(url)


def test_function():
    print("Hello tester")
    assert 6 == 6
