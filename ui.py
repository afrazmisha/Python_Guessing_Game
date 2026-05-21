from engine import NumberGuessingGame
from config import DIFFICULTIES


class GameUI:
    def choose_difficulty(self):
        print("\nSelect Difficulty:")

        for k, v in DIFFICULTIES.items():
            print(f"{k}. {v['name']}")

        choice = input("Choice: ")
        return DIFFICULTIES[choice]

    def play(self):
        settings = self.choose_difficulty()

        engine = NumberGuessingGame(
            settings["max_number"],
            settings["max_attempts"]
        )

        engine.start()

        attempts = 0

        print(f"\nGuess between 1 and {settings['max_number']}")

        while attempts < settings["max_attempts"]:
            guess = int(input("Enter guess: "))
            attempts += 1

            result = engine.check_guess(guess)

            if result == "high":
                print("Too High")
            elif result == "low":
                print("Too Low")
            else:
                print("Correct!")
                print(f"Attempts: {attempts}")
                return True

        print(f"Game Over! Number was {engine.secret_number}")
        return False