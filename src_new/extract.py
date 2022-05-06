from chessdotcom import get_player_game_archives
import requests
import pandas as pd


def data_extract(username, filepath):
    '''Extracts user data for a given username.

    Args:
        username: specified username input.
    Returns:
        outputs a csv file of the users pgn game data.
    '''
    urls = get_player_game_archives(username).json
    all_games = []
    for url in urls["archives"]:
        data = requests.get(url).json()
        for game_pgn in data["games"]:
            chess_game_string = str(game_pgn["pgn"])
            all_games.append(chess_game_string)

    game_dict = {"game_data": all_games}
    df = pd.DataFrame(game_dict, columns=["game_data"])
    df.to_csv(filepath, index=False)
