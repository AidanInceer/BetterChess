"""Progress bars for printing analysis progress."""

from datetime import datetime


def simple_progress_bar(num, total, type) -> None:
    """Simple progress bar."""
    if type == 0:
        x = "of User's data extracted"
    elif type == 1:
        x = "of User's games analysed"
    """Creates a progress bar and estimates time to completion."""
    percent = 100 * ((num + 1) / float(total))
    bar = "❚" * int(percent/2.5) + "-" * (40-int(percent/2.5))
    print(f"\r| {bar}| {percent:.2f}% {x}", end="\r")


def progress_bar(game_num: int,
                 total_games: int,
                 start_time: datetime,
                 end_time: datetime) -> None:
    """Creates a progress bar and estimates time to completion."""
    avg_game_time = timers(start_time, end_time)
    time_r = ((total_games-(game_num+1))*(avg_game_time))/3600
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
    percent = 100 * ((game_num + 1) / float(total_games))
    bar = "❚" * int(percent/2.5) + "-" * (40-int(percent/2.5))
    print(f"\r|{bar}| {percent:.2f}% | ETA: {eta} | Game: {game_num + 1} / {total_games} ", end="\r")


def timers(start_time: datetime, end_time: datetime, time_list: list = []) -> float:
    """time taken to analyse a chess gmae - used to calculate the time remaining for analysis."""
    analysis_time = end_time - start_time
    time_list.append(analysis_time)
    avg_game_time = sum(time_list)/len(time_list)
    return avg_game_time
