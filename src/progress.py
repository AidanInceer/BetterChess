"""Progress bars for printing analysis progress."""

from datetime import datetime


def progress_bar(g: int,
                 t: int,
                 start_time: datetime,
                 end_time: datetime) -> None:
    """Creates a progress bar and estimates time to completion."""
    avg_game_time = timers(start_time, end_time)
    time_r = ((t - (g + 1)) * (avg_game_time))/3600
    hours_r = int(time_r)
    if hours_r < 10:
        hrs = "0" + str(hours_r)
    else:
        hrs = str(hours_r)
    mins_tot = (time_r - hours_r) * 60
    mins_r = int(mins_tot)
    if mins_r < 10:
        mins = "0" + str(mins_r)
    else:
        mins = str(mins_r)
    sec_r = int((mins_tot - mins_r)*60)
    if sec_r < 10:
        secs = "0" + str(sec_r)
    else:
        secs = str(sec_r)
    eta = f"{hrs}:{mins}:{secs}"
    per = 100 * ((g + 1) / float(t))
    bar = "❚" * int(per / 2.5) + "-" * (40-int(per/2.5))
    print(f"\r|{bar}| {per:.2f}% | ETA: {eta} Game: {g + 1} / {t} ", end="\r")


def timers(start_time: datetime, end_time: datetime,
           time_list: list = []) -> float:
    """
    time taken to analyse a chess gmae - used
    to calculate the time remaining for analysis.
    """
    analysis_time = end_time - start_time
    time_list.append(analysis_time)
    avg_game_time = sum(time_list)/len(time_list)
    return avg_game_time
