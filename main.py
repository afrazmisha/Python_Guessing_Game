import random

print("Choose difficulty:")
print("1. Easy (1–50, 10 tries)")
print("2. Medium (1–100, 7 tries)")
print("3. Hard (1–200, 5 tries)")

choice = input("Select (1/2/3): ")

# Difficulty setup
if choice == "1":
    secret_number = random.randint(1, 50)
    max_attempts = 10

elif choice == "2":
    secret_number = random.randint(1, 100)
    max_attempts = 7

else:
    secret_number = random.randint(1, 200)
    max_attempts = 5

print("I picked a number!")

guess = 0
attempts = 0

# Game loop
while guess != secret_number and attempts < max_attempts:

    while True:
        try:
            guess = int(input("Enter your guess: "))
            break
        except ValueError:
            print("Please enter a valid number.")

    attempts += 1

    if guess > secret_number:
        print("Too high!")

    elif guess < secret_number:
        print("Too low!")

# Final result
if guess == secret_number:
    print("Correct!")
    print("Attempts used:", attempts)

else:
    print("Game Over!")
    print("The number was:", secret_number)