from engine import NumberGuessingGame
from config import DIFFICULTIES

class GameService:

    @staticmethod
    def create_game(difficulty_key):
        settings = DIFFICULTIES[difficulty_key]

        game = NumberGuessingGame(
            settings["min_number"],
            settings["max_number"],
            settings["max_attempts"]
        )

        return game
    
    @staticmethod
    def restore_game(session_data):
        return NumberGuessingGame.restore(session_data)
    
    @staticmethod
    def process_guess(game, guess):
        return game.check_guess(guess)
    
    @staticmethod
    def restart_game(game):
        return NumberGuessingGame(
            game.min_number,
            game.max_number,
            game.max_attempts
        )
        return game