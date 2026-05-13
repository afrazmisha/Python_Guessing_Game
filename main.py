import random

class NumberGuessingGame:
    def __init__(self):
        self.secret_number = None
        self.max_attempts = None

    def get_settings(self):

        choice = input("Select difficulty (1/2/3): ")

        if choice == "1":
            self.secret_number = random.randint(1, 10)
            self.max_attempts = 5

        elif choice == "2":
            self.secret_number = random.randint(1, 10)
            self.max_attempts = 3

        else:
            self.secret_number = random.randint(1, 10)
            self.max_attempts = 1

    def play_game(self):
        guess = 0
        attempts = 0

        while guess != self.secret_number and attempts < self.max_attempts:
            
            while True:
                try:
                    guess = int(input("Enter your guess: "))
                    break
                except ValueError:
                    print("Enter a valid number")

            attempts += 1

            if guess > self.secret_number:
                print("Too High")
            elif guess < self.secret_number:
                print("Too Low")

        return guess == self.secret_number, attempts
    
    def run(self):
        play_again = "yes"

        while play_again == "yes":
            self.get_settings()

            print("Game Started!")

            won, attempts = self.play_game()

            if won:
                print("Correct!")
                print("Attempts: ", attempts)
            else:
                print("Game Over!")
                print("Number was: ", self.secret_number)

            play_again = input("Play again? (yes/no): ")

game = NumberGuessingGame()
game.run()