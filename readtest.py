import sqlite3
import pandas as pd

sql_query = """select Game_pgn from game_data where Game_number=5"""
conn = sqlite3.connect("./data/betterchess.db")
all_games = pd.read_sql(sql=sql_query, con=conn)
conn.close
game = all_games["Game_pgn"][0]
data = game.split(r"\n',")


with open(file="basething.txt", mode="w") as file1:
    for line in data:
        file1.write(line.replace(" '", "").replace("['", "").replace(r"\n']", ""))
        file1.write('\n')
