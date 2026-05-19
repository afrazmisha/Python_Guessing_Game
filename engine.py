import random
from config import DIFFICULTIES

class NumberGuessingGame:
    def __init__(self):
        self.secret_number = None
        self.max_attempts = None
        self.max_number = None
        self.base_score = 0
        self.score = 0
        self.best_score = self.load_best_score()

    def get_settings(self):
        while True:
            print("Select Difficulty")
            
            for key, settings in DIFFICULTIES.items():
                print(f"{key}. {settings['name']}")
            
            choice = input("Select Difficulty: ")

            if choice in DIFFICULTIES:
                break

            print("Invalid choice. Try again.")

        settings = DIFFICULTIES[choice]
        
        self.max_number = settings["max_number"]
        self.max_attempts = settings["max_attempts"]
        self.base_score = settings["base_score"]

        self.secret_number = random.randint(1, self.max_number)
        
        print(f"Guess a number between 1 and {self.max_number}")
        print(f"Attempts allowed: {self.max_attempts}")

    def play_game(self):
        guess = None
        attempts = 0

        while attempts < self.max_attempts:

            while True:
                try:
                    guess = int(input("Enter your guess: "))
                    break
                except ValueError:
                    print("Enter a valid number")

            attempts += 1
            remaining = self.max_attempts - attempts

            if guess > self.secret_number:
                print("Too High")
            elif guess < self.secret_number:
                print("Too Low")
            else:
                break

            if remaining > 0:
                print("Attempts remaining:", remaining)

        return guess == self.secret_number, attempts

    def run(self):
        while True:
            self.get_settings()
            print("\nGame Started!")

            won, attempts = self.play_game()

            if won:
                self.score = self.base_score - (attempts * 10)

                print("Correct!")
                print("Attempts: ", attempts)
                print("Score: ", self.score)
                print("Best Score: ", self.best_score)

                if self.score > self.best_score:
                    print("New High Score!")
                    self.best_score = self.score
                    self.save_best_score(self.best_score)
                    
            else:
                print("Game Over! Number was:", self.secret_number)

            again = input("Play again? (yes/no): ").strip().lower()
            if again != "yes":
                break

    def load_best_score(self):
        try:
            with open("score.txt", "r") as file:
                return int(file.read().strip())
        except:
            return 0
        
    def save_best_score(self, score):
        with open("score.txt", "w") as file:
            file.write(str(score))
