from flask import Flask, render_template, request, redirect, url_for, session
from engine import NumberGuessingGame
from config import DIFFICULTIES

app = Flask(__name__)
app.secret_key = "secret-key"

@app.route("/")
def index():
    return render_template(
        "index.html",
        difficulties=DIFFICULTIES,
        game_started=False,
        result=None
    )

@app.route("/start", methods=["POST"])
def start():
    difficulty = request.form["difficulty"]

    settings = DIFFICULTIES[difficulty]

    game = NumberGuessingGame(
        settings["min_number"],
        settings["max_number"],
        settings["max_attempts"]
    )

    session["secret_number"] = game.secret_number
    session["attempts"] = game.attempts
    session["max_attempts"] = game.max_attempts
    session["min_number"] = game.min_number
    session["max_number"] = game.max_number
    session["game_over"] = game.game_over

    
    return render_template(
        "index.html",
        game_started=True,
        min_number=game.min_number,
        max_number=game.max_number,
        attempts_left=game.max_attempts
    )

@app.route("/guess", methods=["POST"])
def guess():
    user_guess = int(request.form["guess"])

    game = NumberGuessingGame(
        session["min_number"],
        session["max_number"],
        session["max_attempts"]
    )

    game.secret_number = session["secret_number"]
    game.attempts = session["attempts"]
    game.game_over = session["game_over"]

    result = game.check_guess(user_guess)

    session["attempts"] = game.attempts
    session["game_over"] = game.game_over

    return render_template(
        "index.html",
        game_started=True,
        min_number=game.min_number,
        max_number=game.max_number,
        result=result,
        attempts_left=max(0, game.max_attempts - game.attempts)
    )

if __name__ == "__main__":
    app.run(debug=True)