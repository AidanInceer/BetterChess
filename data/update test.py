from chessdotcom import get_player_game_archives
import requests
import pandas as pd
import sqlalchemy
import pprint
from datetime import datetime

printer = pprint.PrettyPrinter()



def data_extract_test(username):

    currentmonth = datetime.now().month
    currentyear = datetime.now().year

    # Getting game data from Chess.com
    urls = get_player_game_archives(username).json

    month_url = f"https://api.chess.com/pub/player/{username}/games/{currentyear}/0{currentmonth}"
    data = requests.get(month_url).json()

    print("done")

    # Iterate through all games within each month
    #     for game_pgn in data["games"]:
    #         # Add in game data to list
    #         chess_game_string = str(game_pgn["pgn"])
    #         all_games.append(chess_game_string)


data_extract_test("Ainceer")
