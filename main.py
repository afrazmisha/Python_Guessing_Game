def get_settings():
    import random

    choice = input("Select difficulty (1/2/3): ")

    if choice == "1":
        return random.randint(1, 10), 5
    elif choice == "2":
        return random.randint(1, 10), 3
    else:
        return random.randint(1, 10), 1
    
def play_game(secret_number, max_attemps):
        guess = 0
        attempts = 0

        while guess != secret_number and attempts < max_attempts:

            while True:
                try:
                    guess = int(input("Enter your guess: "))
                    break
                except ValueError:
                    print("Enter a valid number")

            attempts += 1

            if guess > secret_number:
                print("Too High")
            elif guess < secret_number:
                print("Too Low")

        return guess == secret_number, attempts

secret_number, max_attempts = get_settings()

print("Game started!")

won, attempts = play_game(secret_number, max_attempts)

if won:
    print("Correct!")
    print("Attempts: ", attempts)
else:
    print("Game Over!")
    print("Number was: ", secret_number)
