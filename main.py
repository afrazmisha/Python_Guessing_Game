from ui import GameUI

game = GameUI()

while True:
    result = game.play()

    again = input("\nPlay again? (yes/no): ").strip().lower()

    if again != "yes":
        print("Goodbye 👋")
        break