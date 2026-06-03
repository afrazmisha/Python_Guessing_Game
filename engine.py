import random

class NumberGuessingGame:
    def __init__(self, min_number, max_number, max_attempts):
        if None in (min_number, max_number, max_attempts):
            raise ValueError("Invalid initialization")

        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts

        self.secret_number = random.randint(min_number, max_number)

        self.attempts = 0
        self.game_over = False
        self.last_result = None

    def _response(self, status, message):
        return {
            "status": status,
            "message": message,
            "attempts": self.attempts,
            "attempts_left": self.max_attempts - self.attempts,
            "secret_number": self.secret_number
        }

    def check_guess(self, guess):
        if self.game_over:
            return self._response ("finished", "Game already ended")
        
        self.attempts += 1

        if guess == self.secret_number:
            self.game_over = True
            self.last_result = "won"
            return self._response("won", "Correct!")

        if self.attempts >= self.max_attempts:
            self.game_over = True
            self.last_result = "lost"
            return self._response("lost", f"Game Over! Number was {self.secret_number}")

        if guess < self.secret_number:
            return self._response("continue", "Too Low")

        return self._response("continue", "Too High")

    def serialize(self):
        return {
            "min_number": self.min_number,
            "max_number": self.max_number,
            "max_attempts": self.max_attempts,
            "secret_number": self.secret_number,
            "attempts": self.attempts,
            "game_over": self.game_over,
            "last_result": self.last_result
        }

    @staticmethod
    def restore(data):
        game = NumberGuessingGame(
            data["min_number"],
            data["max_number"],
            data["max_attempts"]
        )

        game.secret_number = data["secret_number"]
        game.attempts = data.get("attempts", 0)
        game.game_over = data.get("game_over", False)
        game.last_result = data.get("last_result")

        return game