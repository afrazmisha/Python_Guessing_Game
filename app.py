from flask import Flask, render_template, request, redirect, url_for, session
from engine import NumberGuessingGame
from config import DIFFICULTIES

app = Flask(__name__)
app.secret_key = "secret-key"

@app.route("/")
def index():
    return render_template(
        "index.html",
        difficulties=DIFFICULTIES
    )

@app.route("/start", method=["POST"])
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

    
    return render_template(
        "index.html",
        game_started=True,
        min_number=game.min_number,
        max_number=game.max_number,
        attempts_left=game.max_attempts
    )

@app.route("/guess", method=["POST"])
def guess():
    user_guess = int(request.form["guess"])

    game = NumberGuessingGame(
        session["min_number"],
        session["max_number"],
        session["max_attempts"]
    )

    game.secret_number = session["secret_number"]
    game.attempts = session["attempts"]

    result = game.check_guess(user_guess)

    session["attempts"] = game.attempts

    return render_template(
        "index.htmml",
        game_started=True,
        min_number=game.min_number,
        max_number=game.max_number,
        result=result,
        attempts_left=game.max_attempts - game.attempts
    )

if __name__ == "__main__":
    app.run(debug=True)