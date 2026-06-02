from engine import NumberGuessingGame
from config import DIFFICULTIES

class GameUI:
    def choose_difficulty(self):
        print("\nSelect Difficulty:")

        for k, v in DIFFICULTIES.items():
            print(f"{k}. {v['name']}")

        while True:
            choice = input("Choice: ").strip()

            if choice in DIFFICULTIES:
                return DIFFICULTIES[choice]

            print("Invalid choice. Try again.")

    def play(self):
        settings = self.choose_difficulty()

        engine = NumberGuessingGame(
            settings["min_number"],
            settings["max_number"],
            settings["max_attempts"]
        )

        print(f"\nGuess between {engine.min_number} and {engine.max_number}")

        while not engine.game_over:
            try:
                guess = int(input("Enter guess: "))

                if guess < engine.min_number or guess > engine.max_number:
                    print(
                        f"Enter number between "
                        f"{engine.min_number} and {engine.max_number}"
                    )
                    continue

            except ValueError:
                print("Enter a valid number")
                continue

            result = engine.check_guess(guess)

            print(result["message"])

            if result["status"] in ["won", "lost"]:
                print(f"Attempts used: {engine.attempts}")
                return result

        return {
            "status": "lost"
        }