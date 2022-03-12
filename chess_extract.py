from chessdotcom import get_player_game_archives
import requests
import pandas as pd


def data_extract(username="Ainceer"):
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
    df.to_csv(".\data\game_data_pgn.csv",index=False)
