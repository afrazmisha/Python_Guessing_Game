from flask import Flask, render_template, request, session, redirect, url_for
from engine import NumberGuessingGame
from config import DIFFICULTIES

app = Flask(__name__)
app.secret_key = "secret-key"

@app.route("/")
def index():
    return render_template(
        "index.html",
        state="start",
        difficulties=DIFFICULTIES,
    )

#COMPLETED
@app.route("/start", methods=["POST"])
def start():
    settings = DIFFICULTIES[request.form["difficulty"]]

    game = NumberGuessingGame(
        settings["min_number"],
        settings["max_number"],
        settings["max_attempts"]
    )

    session["game"] = game.serialize()

    return render_template(
        "play.html",
        game=game,
        min_number=game.min_number,
        max_number=game.max_number,
        attempts_left=game.max_attempts - game.attempts,
        result=None
    )

#COMPLETED
@app.route("/guess", methods=["POST"])
def guess():
    if "game" not in session:
        return redirect(url_for("index"))

    game = NumberGuessingGame.restore(session["game"])
    result = game.check_guess(int(request.form["guess"]))

    session["game"] = game.serialize()

    if result["status"] in ["won", "lost"]:
        return redirect(url_for("end"))

    return render_template(
        "play.html",
        game=game,
        result=result,
        min_number=game.min_number,
        max_number=game.max_number,
        attempts_left=game.max_attempts - game.attempts
    )

#COMPLETED
@app.route("/end")
def end():
    if "game" not in session:
        return redirect(url_for("index"))
    
    game = NumberGuessingGame.restore(session["game"])

    return render_template(
        "end.html",
        game=game,
        won=(game.last_result == "won"),
        secret_number=game.secret_number,
        attempts=game.attempts
    )
    
#COMPLETED    
@app.route("/restart", methods=["POST"])
def restart():
    if "game" not in session:
        return redirect(url_for("index"))

    # 1. restore existing game state
    game = NumberGuessingGame.restore(session["game"])

    # 2. reset it properly (NEW ROUND, SAME SETTINGS)
    game.reset_for_new_round()

    # 3. save back into session
    session["game"] = game.serialize()

    return redirect(url_for("index"))

@app.route("/exit", methods=["POST"])
def exit_game():
    session.clear()
    return render_template("goodbye.html")

if __name__ == "__main__":
    app.run(debug=True)