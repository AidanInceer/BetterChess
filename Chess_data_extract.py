from chessdotcom import get_player_game_archives
import requests
import pandas as pd
import sqlalchemy


def data_extract(username):
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
    engine = sqlalchemy.create_engine('mysql+pymysql://root:password@localhost:3306/chess_raw_data')
    df.to_sql(
        name='all_games_data',
        con=engine,
        index=False,
        if_exists='replace'
    )


data_extract("Ainceer")
