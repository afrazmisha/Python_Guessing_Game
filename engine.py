import random

class NumberGuessingGame:
    def __init__(self):
        self.secret_number = None
        self.max_attempts = None
        self.max_number = None

    def get_settings(self):
        while True:
            print("Select Difficulty - Easy (1), Medium (2), Hard (3): ")
            choice = input("Select (1/2/3): ")

            if choice in ["1", "2", "3"]:
                break
            print("Invalid choice. Try again.")

        if choice == "1":
            self.max_number = 10
            self.max_attempts = 5
        elif choice == "2":
            self.max_number = 50
            self.max_attempts = 3
        else:
            self.max_number = 100
            self.max_attempts = 2

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
                print("Correct!")
            else:
                print("Game Over! Number was:", self.secret_number)

            again = input("Play again? (yes/no): ").strip().lower()
            if again != "yes":
                break