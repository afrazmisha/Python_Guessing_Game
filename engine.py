import random

class NumberGuessingGame:
    def __init__(self, min_number, max_number, max_attempts):
        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts

        self.secret_number = random.randint(min_number, max_number)

        self.attempts = 0
        self.game_over = False
        self.last_result = None

    def check_guess(self, guess):
        if self.game_over:
            return {
                "message": "Game already ended!",
                "status": "finished"
            }

        self.attempts += 1

        # Too Low
        if guess < self.secret_number:
            self.last_result = "continue"
            result = "Too Low"
        
        # Too High
        elif guess > self.secret_number:
            self.last_result = "continue"
            result = "Too High"
        
        # Correct guess
        else:
            self.game_over = True
            self.last_result = "won"
            
            return {
                "message": "Correct!",
                "status": "won",
                "attempts": self.attempts
            }
        # Loss condition
        if self.attempts >= self.max_attempts:
            self.game_over = True
            self.last_result = "lost"

            return {
                 "message": f"Game Over! Number was {self.secret_number}",
                 "status": "lost",
                 "attempts": self.attempts
            }
        
        # Continue Game
        return {
             "message": result,
             "status": "continue",
             "attempts_left": self.max_attempts - self.attempts
        }
    
    def reset_for_new_round(self):
         self.secret_number = random.randint(
              self.min_number,
              self.max_number
         )

         self.attempts = 0
         self.game_over = False
         self.last_result = None
        
    def serialize(self):
            return {
                 "min": self.min_number,
                 "max": self.max_number,
                 "max_attempts": self.max_attempts,
                 "secret_number": self.secret_number,
                 "attempts": self.attempts,
                 "game_over": self.game_over,
                 "last_result": self.last_result
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
            game.last_result = data.get("last_result")
            
            return game