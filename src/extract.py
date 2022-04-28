from chessdotcom import get_player_game_archives
import requests
import pandas as pd
import os

username = "LucidKoala"
dirname = os.path.dirname(__file__)


def data_extract(username=username):
    '''Extracts user data for a given username.

    Args:
        username: specified username input.
    Returns:
        outputs a csv file of the users pgn game data.
    '''
    # file paths
    filename = os.path.join(dirname, rf"../data/{username}_pgn_data.csv")
    # Getting game data from Chess.com
    urls = get_player_game_archives(username).json
    # Iterate through each months data
    all_games = []
    for url in urls["archives"]:
        data = requests.get(url).json()
        # Iterate through all games within each month
        for game_pgn in data["games"]:
            # Add in game data to list
            chess_game_string = str(game_pgn["pgn"])
            all_games.append(chess_game_string)
    game_dict = {"game_data": all_games}
    df = pd.DataFrame(game_dict, columns=["game_data"])
    df.to_csv(filename, index=False)
