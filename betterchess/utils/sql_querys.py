DROP_MOVE_TABLE = """DROP TABLE IF EXISTS move_data"""
DROP_GAME_TABLE = """DROP TABLE IF EXISTS game_data"""
DROP_PGN_TABLE = """DROP TABLE IF EXISTS pgn_data"""
CREATE_MOVE_TABLE = """
    CREATE TABLE move_data (
    Username TEXT,
    Game_date TEXT,
    Engine_depth INTEGER,
    Game_number INTEGER,
    Move_number INTEGER,
    Move TEXT,
    Move_eval INTEGER,
    Best_move TEXT,
    Best_move_eval INTEGER,
    Move_eval_diff INTEGER,
    Move_accuracy REAL,
    Move_type TEXT,
    Piece TEXT,
    Move_colour TEXT,
    Castling_type TEXT,
    White_castle_num INTEGER,
    Black_castle_num INTEGER,
    Move_time REAL
)"""
CREATE_GAME_TABLE = """
    CREATE TABLE game_data (
    Username TEXT,
    Game_date TEXT,
    Game_time_of_day TEXT,
    Game_weekday TEXT,
    Engine_depth INT,
    Game_number INT,
    Game_type TEXT,
    White_player TEXT,
    White_rating INT,
    Black_player TEXT,
    Black_rating INT,
    User_colour TEXT,
    User_rating INT,
    Opponent_rating INT,
    User_win_percent REAL,
    Opp_win_percent REAL,
    User_winner TEXT,
    Opening_name TEXT,
    Opening_class TEXT,
    Termination TEXT,
    End_type TEXT,
    Number_of_moves INT,
    Accuracy REAL,
    Opening_accuracy REAL,
    Mid_accuracy REAL,
    End_accuracy REAL,
    No_best INT,
    No_excellent INT,
    No_good INT,
    No_inaccuracy INT,
    No_mistake INT,
    No_blunder INT,
    No_missed_win INT,
    Improvement TEXT,
    User_castle_num INT,
    Opp_castle_num INT,
    User_castled INT,
    Opp_castled INT,
    User_castle_phase INT,
    Opp_castle_phase INT
)"""
CREATE_PGN_TABLE = """
    CREATE TABLE pgn_data (
    username TEXT,
    url_date TEXT,
    game_data TEXT
)"""
SELECT_MOVE_DATA = """SELECT * FROM move_data limit 10"""
SELECT_GAME_DATA = """SELECT * FROM game_data limit 10"""
SELECT_PGN_DATA = """SELECT * FROM pgn_data limit 1"""

SELECT_MOVE_DATA_ALL = """SELECT * FROM move_data"""
SELECT_GAME_DATA_ALL = """SELECT * FROM game_data"""
SELECT_PGN_DATA_ALL = """SELECT * FROM pgn_data"""
