from flask import Flask, render_template, request, session, redirect, url_for 
from engine import NumberGuessingGame
from config import DIFFICULTIES
import random

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

    session["game"] = game.serialize()
    
    return render_template(
        "index.html",
        game_started=True,
        game_over=False,
        min_number=game.min_number,
        max_number=game.max_number,
        attempts_left=game.max_attempts
    )

@app.route("/guess", methods=["POST"])
def guess():
    if "game" not in session:
        return redirect(url_for("index"))
    
    user_guess = int(request.form["guess"])

    game = NumberGuessingGame.restore(session["game"])

    result = game.check_guess(user_guess)

    session["game"] = game.serialize()
    session["result"] = result

    if game.game_over:
        return redirect(url_for("end"))

    return render_template(
        "index.html",
        game_started=True,
        result=result,
        min_number=game.min_number,
        max_number=game.max_number,
        attempts_left=max(0, game.max_attempts - game.attempts),
        difficulties=DIFFICULTIES
    )

@app.route("/end")
def end():
    if "game" not in session:
        return redirect(url_for("index"))
    
    game = NumberGuessingGame.restore(session["game"])

    return render_template(
        "end.html",
        won=game.last_result == "won",
        secret_number=game.secret_number,
        attempts=game.attempts
    )

@app.route("/reset", methods=["POST"])
def reset():
    choice = request.form["choice"]

    if choice == "exit":
        session.clear()
        return "See you soon 👋"
    
    if choice == "change":
        session.clear()
        return redirect(url_for("index"))
    
    if choice == "same":
        game = NumberGuessingGame.restore(session["game"])
        game.reset_for_new_round()

        session["game"] = game.serialize()

        return redirect(url_for("guess_page"))

if __name__ == "__main__":
    app.run(debug=True)