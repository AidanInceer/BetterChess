
# user has chess games which have moves


class User():
    user_number = 0

    def __init__(self, username, name, user_rating, location):
        self.username = username
        self.name = name
        self.user_rating = user_rating
        self.location = location
        User.user_number += 1


class ChessGame(User):
    game_number = 0

    def __init__(self, username, name, user_rating, location, time_control,
                 white, black, player, white_rating, black_rating,
                 opening_class, opening_name, result, user_winner,
                 game_datetime, total_moves):
        super().__init__(username, name, user_rating, location)
        self.time_control = time_control
        self.white = white
        self.black = black
        self.player = player
        self.white_rating = white_rating
        self.black_rating = black_rating
        self.opening_class = opening_class
        self.opening_name = opening_name
        self.result = result
        self.user_winner = user_winner
        self.game_datetime = game_datetime
        self.total_moves = total_moves
        User.ChessGame.game_number += 1


class move(ChessGame):
    pass