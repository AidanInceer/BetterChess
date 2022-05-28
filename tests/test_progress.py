from src import progress


def test_progress_bar():
    pass


def test_timer():
    timer = 1
    st = 1
    et = 2
    tl = []
    assert timer == progress.timers(st, et, tl)
