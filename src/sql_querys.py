DROP_MOVE_TABLE = """DROP TABLE IF EXISTS move_data"""
DROP_GAME_TABLE = """DROP TABLE IF EXISTS game_data"""
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
    Engine_depth INTEGER,
    Game_number INTEGER,
    Game_type TEXT,
    White_player TEXT,
    Black_player TEXT,
    White_rating INTEGER,
    Black_rating INTEGER,
    User_colour TEXT,
    User_rating INTEGER,
    Opponent_rating INTEGER,
    User_winner TEXT,
    Opening_name TEXT,
    Opening_class TEXT,
    Termination TEXT,
    End_type TEXT,
    Number_of_moves INTEGER,
    Accuracy REAL,
    Opening_accuracy REAL,
    Mid_accuracy REAL,
    End_accuracy REAL,
    No_best INTEGER,
    No_excellent INTEGER,
    No_good INTEGER,
    No_inaccuracy INTEGER,
    No_mistake INTEGER,
    No_blunder INTEGER,
    No_missed_win INTEGER,
    Improvement TEXT,
    User_castle_num INTEGER,
    Opp_castle_num INTEGER,
    User_castled INTEGER,
    Opp_castled INTEGER,
    User_castle_phase TEXT,
    Opp_castle_phase TEXT
)"""

DELETE_WHERE_GAME_NUM_AND_USER_EQUAL = """
    DELETE FROM :table
    WHERE Game_number = :game_num and Username = :username
"""

SELECT_MOVE_DATA = """SELECT * FROM move_data limit 10"""
SELECT_GAME_DATA = """SELECT * FROM game_data limit 10"""
