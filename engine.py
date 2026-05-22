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

            if guess > self.secret_number:
                result = "Too High"
            elif guess < self.secret_number:
                result = "Too Low"
            else:
                self.game_over = True

                return {
                    "message": "Correct!",
                    "status": "won",
                    "attempts": self.attempts
                }
            
            if self.attempts >= self.max_attempts:
                self.game_over = True

                return {
                    "message": f"Game Over! Number was {self.secret_number}",
                    "status": "lost"
                }
            
            return {
                "message": result,
                "status": "continue",
                "attempts_left": self.max_attempts - self.attempts
            }