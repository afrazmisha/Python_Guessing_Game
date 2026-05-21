import random

class NumberGuessingGame:
    def __init__(self, max_number, max_attempts):
        self.max_number = max_number
        self.max_attempts = max_attempts
        self.secret_number = None

    def start(self):
        self.secret_number = random.randint(1, self.max_number)

    def check_guess(self, guess):
        if guess > self.secret_number:
            return "high"
        elif guess < self.secret_number:
            return "low"
        else:
            return "correct"