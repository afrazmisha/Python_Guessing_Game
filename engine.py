import random

class NumberGuessingGame:
    def __init__(self, min_number, max_number, max_attempts):
        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts

        self.secret_number = random.randint(min_number, max_number)

        self.attempts = 0
        self.game_over = False

    def check_guess(self, guess):
        if self.game_over:
            return {
                "message": "Game already ended!",
                "status": "finished"
            }

        self.attempts += 1

        #Too Low
        if guess < self.secret_number:
            self.last_result = "continue"
            return self._handle_continue("Too Low")
        
        if guess > self.secret_number:
            return self._handle_continue("Too High")
        
        self.game_over = True
        self.last_result = "won" /"lost" /"continue"
        return {
             "message": "Correct!",
             "status": "won",
             "attempts": self.attempts
             }
    
    def _handle_continue(self, message):
        if self.attempts >= self.max_attempts:
            self.game_over = True
            return {
                "message": f"Game Over! Number was {self.secret_number}",
                "status": "lost"
            }
        
        return {
            "message": message,
            "status": "continue",
            "attempts_left": self.max_attempts - self.attempts
            }
        
    def serialize(self):
            return {
                 "min": self.min_number,
                 "max": self.max_number,
                 "max_attempts": self.max_attempts,
                 "secret_number": self.secret_number,
                 "attempts": self.attempts,
                 "game_over": self.game_over
            }
    
    @staticmethod
    def restore(data):
            game = NumberGuessingGame(
                 data["min"],
                 data["max"],
                 data["max_attempts"]
            )

            game.secret_number = data["secret_number"]
            game.attempts = data["attempts"]
            game.game_over = data["game_over"]
            return game