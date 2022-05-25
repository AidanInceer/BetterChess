"""Extracts the data of a given chess.com user."""
import pandas as pd
import requests
from chessdotcom import get_player_game_archives
from datetime import datetime
from logging import Logger


def data_extract(username: str, filepath: str, logfilepath: str, logger: Logger) -> None:
    '''Extracts user data for a given username.
    Args:
        username: specified username input.
        filepath: filepath for csv storage.
        extlogger: extract logger.
    Returns:
        outputs a csv file of the users pgn game data.
    '''
    init_dt = "2000-01-01 00:00:00"
    init_extlogger = datetime.strptime(init_dt, '%Y-%m-%d %H:%M:%S')
    logger.info(f"| {init_extlogger}")
    urls = get_player_game_archives(username).json
    url_date_list = []
    games_list = []
    tot_urls = len(urls["archives"])
    print("Extracting users data: ")
    for url_num, url in enumerate(urls["archives"]):
        simple_progress_bar(url_num, tot_urls, 0)
        in_curr = in_curr_month(url)
        in_log = url_in_log(url, logfilepath)
        url_date = get_url_date(url)
        logger.info(f"| {url_date}")
        url_games_list = extract_filter(
            in_log, in_curr, url, filepath, logfilepath)
        try:
            for game in url_games_list:
                url_date_list.append(url_date)
                games_list.append(game)
        except TypeError:
            continue
    print("\n")
    game_dict = {"url_date": url_date_list,
                 "game_data": games_list}
    df = pd.DataFrame(game_dict)
    df.to_csv(filepath, mode="a", index=False, sep="|", header=False)


def extract_filter(in_log: bool,
                   in_curr: bool,
                   url: str,
                   filepath: str,
                   logfilepath: str) -> list:
    """Filter to remove any incomplete games"""
    empty_list = []
    if not in_log:
        return collect_game_data(url)
    elif in_log and not in_curr:
        return empty_list
    elif in_log and in_curr:
        filter_pgncsv(filepath, logfilepath)
        return empty_list


def filter_pgncsv(filepath: str, logfilepath: str) -> None:
    """Removes games of the current month in the csv
     and then reruns the extract for that month."""
    # Opens logging file
    with open(logfilepath, "r") as log_file:
        lines = log_file.readlines()
    llog = lines[-1]
    llog_dt = llog.split("|")[1].strip()
    col_names = ["url_date", "game_data"]
    unclean_df = pd.read_csv(
        filepath,
        names=col_names,
        delimiter="|",
        header=None)
    df_filter = unclean_df["url_date"] != llog_dt
    clean_df = unclean_df[df_filter]
    clean_df.to_csv(
        filepath,
        mode="w",
        sep="|",
        index=False,
        header=None)


def collect_game_data(url: str) -> list:
    """returns a list of all the users chess games."""
    data = requests.get(url).json()
    url_games_list = []
    for game_pgn in data["games"]:
        chess_game_string = str(game_pgn["pgn"]).replace("\n", " ; ")
        url_games_list.append(chess_game_string)
    return url_games_list


def url_in_log(url: str, logfilepath: str) -> bool:
    """Checks to see if the url is allready in the logfile"""
    url_date = get_url_date(url)
    with open(logfilepath, "r") as log_file:
        lines = log_file.readlines()
    url_date_list = []
    for line in lines:
        log_url_date = datetime.strptime(
            line.split("|")[1].strip(),
            '%Y-%m-%d %H:%M:%S')
        url_date_list.append(log_url_date)
    if url_date in url_date_list:
        return True
    else:
        return False


def in_curr_month(url: str) -> bool:
    """Checks to see if the extracted month equals the current month"""
    url_date = get_url_date(url)
    curr_mth = get_curr_mth()
    if curr_mth == url_date:
        return True
    else:
        return False


def get_curr_mth() -> datetime:
    """Returns the current month."""
    cyv = datetime.now().year
    cmv = datetime.now().month
    curr_mth = datetime.strptime(
        f"{cyv}-{cmv}-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    return curr_mth


def get_url_date(url: str) -> datetime:
    """Returns the date of the url as datatime."""
    x = url.split("/")[7:]
    yr, mth = x[0], x[1]
    url_date = datetime.strptime(
        f"{yr}-{mth}-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    return url_date


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
