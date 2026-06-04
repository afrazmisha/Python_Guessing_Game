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
    
    @staticmethod
    def game_from_state(state):
        game = NumberGuessingGame(
            state.min_number,
            state.max_number,
            state.max_attempts
        )

        game.secret_number = state.secret_number
        game.attempts = state.attempts
        game.game_over = state.game_over
        game.last_result = state.last_result

        return game
    
    @staticmethod
    def update_state_from_game(state, game):
        state.secret_number = game.secret_number
        state.attempts = game.attempts
        state.game_over = game.game_over
        state.last_result = game.last_result

        return state