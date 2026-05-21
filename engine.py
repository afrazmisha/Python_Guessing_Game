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
        
        self.games_played = 0
        self.wins = 0
        self.total_attempts = 0
        
        self.load_stats()

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
        
        print(f"\nGuess a number between 1 and {self.max_number}")
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
                return True, attempts

            if remaining > 0:
                print("Attempts remaining:", remaining)

        return False, attempts

    def run(self):
        while True:
            self.get_settings()
            print("\nGame Started!")

            won, attempts = self.play_game()

            self.games_played += 1
            self.total_attempts += attempts

            if won:
                self.wins += 1
                self.score = max(0, self.base_score - (attempts * 10))

                print("\nCorrect!")
                print("Attempts: ", attempts)
                print("Score: ", self.score)

                if self.score > self.best_score:
                    print("New High Score!")
                    self.best_score = self.score
                    self.save_best_score()

            else:
                print("\nGame Over! Number was:", self.secret_number)

            self.save_stats()
            self.show_stats()

            again = input("Play again? (yes/no): ").strip().lower()
            if again != "yes":
                break


    def show_stats(self):
        if self.games_played == 0:
            return
        
        losses = self.games_played - self.wins
        average_attempts = self.total_attempts / self.games_played
        win_rate = (self.wins / self.games_played) * 100
        
        print("\n=== Statistics ===")
        print("Games Played:", self.games_played)
        print("Wins:", self.wins)
        print("Losses:", losses)
        print(f"Average Attempts: {average_attempts:.2f}")
        print(f"Win Rate: {win_rate:.2f}%")

    def load_best_score(self):
        try:
            with open("score.txt", "r") as f:
                return int(f.read().strip())
        except FileNotFoundError:
            return 0
        
    def save_best_score(self):
        with open("score.txt", "w") as f:
            f.write(str(self.best_score))

    def load_stats(self):
        try:
            with open("stats.txt", "r") as f:
                lines = f.readlines()

                if len(lines) < 3:
                    raise ValueError
                
                self.games_played = int(lines[0])
                self.wins = int(lines[1])
                self.total_attempts = int(lines[2])

        except (FileNotFoundError, ValueError):
            self.games_played = 0
            self.wins = 0
            self.total_attempts = 0
            
    def save_stats(self):
        with open("stats.txt", "w") as f:
            f.write(f"{self.games_played}\n")
            f.write(f"{self.wins}\n")
            f.write(f"{self.total_attempts}\n")