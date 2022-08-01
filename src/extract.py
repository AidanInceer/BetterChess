"""Extracts the data of a given chess.com user."""
import chessdotcom
import pandas as pd
import requests
from datetime import datetime
from logging import Logger
import sqlite3


def data_extract(
    username: str, dbfilepath: str, logfilepath: str, logger: Logger
) -> None:
    """Extracts user data for a given username.
    Args:
        username: specified username input.
        filepath: filepath for csv storage.
        extlogger: extract logger.
    Returns:
        outputs a csv file of the users pgn game data.
    """
    init_dt = "2000-01-01 00:00:00"
    init_extlogger = datetime.strptime(init_dt, "%Y-%m-%d %H:%M:%S")
    logger.info(f"| {username} | {init_extlogger}")
    urls = chessdotcom.get_player_game_archives(username=username).json
    username_list = []
    url_date_list = []
    games_list = []
    tot_urls = len(urls["archives"])
    print("Extracting users data: ")
    for url_num, url in enumerate(urls["archives"]):
        simple_progress_bar(num=url_num, total=tot_urls, type=0)
        in_curr = in_curr_month(url=url)
        in_log = url_in_log(url=url, logfilepath=logfilepath)
        url_date = get_url_date(url=url)
        logger.info(f"| {username} | {url_date}")
        url_games_list = extract_filter(
            username=username,
            in_log=in_log,
            in_curr=in_curr,
            url=url,
            dbfilepath=dbfilepath,
        )
        try:
            for game in url_games_list:
                username_list.append(username)
                url_date_list.append(url_date)
                games_list.append(game)
        except TypeError:
            continue
    print("\n")
    game_dict = {
        "username": username_list,
        "url_date": url_date_list,
        "game_data": games_list,
    }
    game_pgn_data_df = pd.DataFrame(game_dict)
    conn = conn = sqlite3.connect(database=dbfilepath)
    game_pgn_data_df.to_sql(name="pgn_data", con=conn, if_exists="append", index=False)
    conn.commit
    conn.close


def extract_filter(
    username: str,
    in_log: bool,
    in_curr: bool,
    url: str,
    dbfilepath: str,
) -> list:
    """Filter to remove any incomplete games"""
    empty_list = []
    if not in_log:
        return collect_game_data(url=url)
    elif in_log and not in_curr:
        return empty_list
    elif in_log and in_curr:
        filter_pgn_table(username=username, dbfilepath=dbfilepath)
        return collect_game_data(url)


def filter_pgn_table(username: str, dbfilepath: str) -> None:
    """Removes games of the current month in the sql database (pgn_data)
    and then reruns the extract for that month."""
    curr_month = get_curr_mth()
    sql_query = (
        """delete from pgn_data where username=:username and url_date=:curr_month"""
    )
    params = {"username": username, "curr_month": curr_month}
    conn = sqlite3.connect(database=dbfilepath)
    curs = conn.cursor()
    curs.execute(sql_query, params)
    conn.commit
    conn.close


def collect_game_data(url: str) -> list:
    """returns a list of all the users chess games."""
    response = requests.get(url)
    data = response.json()
    url_games_list = []
    for game_pgn in data["games"]:
        chess_game_string = str(game_pgn["pgn"]).replace("\n", " ; ")
        url_games_list.append(chess_game_string)
    return url_games_list


def url_in_log(url: str, logfilepath: str) -> bool:
    """Checks to see if the url is allready in the logfile"""
    url_date = get_url_date(url=url)
    with open(logfilepath, "r") as log_file:
        lines = log_file.readlines()
    url_date_list = []
    for line in lines:
        log_url_date = datetime.strptime(
            line.split("|")[2].strip(), "%Y-%m-%d %H:%M:%S"
        )
        url_date_list.append(log_url_date)
    if url_date in url_date_list:
        return True
    else:
        return False


def in_curr_month(url: str) -> bool:
    """Checks to see if the extracted month equals the current month"""
    url_date = get_url_date(url=url)
    curr_mth = get_curr_mth()
    if curr_mth == url_date:
        return True
    else:
        return False


def get_curr_mth() -> datetime:
    """Returns the current month."""
    cyv = datetime.now().year
    cmv = datetime.now().month
    curr_mth = datetime.strptime(f"{cyv}-{cmv}-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    return curr_mth


def get_url_date(url: str) -> datetime:
    """Returns the date of the url as datatime."""
    x = url.split("/")[7:]
    yr, mth = x[0], x[1]
    url_date = datetime.strptime(f"{yr}-{mth}-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    return url_date


def simple_progress_bar(num: int, total: int, type: int) -> None:
    """Simple progress bar."""
    if type == 0:
        x = "of User's data extracted"
        percent = 100 * ((num + 1) / float(total))
        bar = "❚" * int(percent / 2.5) + "-" * (40 - int(percent / 2.5))
        print(f"\r| {bar}| {percent:.2f}% {x}", end="\r")
    elif type == 1:
        x = "of User's games analysed"
        percent = 100 * ((num + 1) / float(total))
        bar = "❚" * int(percent / 2.5) + "-" * (40 - int(percent / 2.5))
        print(f"\r| {bar}| {percent:.2f}% {x}", end="\r")
