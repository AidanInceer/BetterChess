

def progress_bar(game_num, total_games, start_time, end_time, time_list):

    """Creates a progress bar and estimates time to completion."""
    analysis_time = end_time - start_time
    time_list.append(analysis_time)
    avg_game_time = sum(time_list)/len(time_list)
    time_r = ((total_games-game_num)*(avg_game_time))/3600
    hours_r = int(time_r)
    mins_r = (time_r - hours_r) * 60

    percent = 100 * (game_num / float(total_games))
    bar = "❚" * int(percent) + "-" * (100-int(percent))
    print(f"ETA: {hours_r} Hours,  {mins_r:.1f} Mins | \r|{bar}| {percent:.2f}%", end="\r")