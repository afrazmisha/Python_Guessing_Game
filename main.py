from ui import GameUI

game = GameUI()

while True:
    game.play()

    again = input("\nPlay again? (yes/no): ").lower()
    if again != "yes":
        break