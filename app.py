from flask import Flask, render_template, request, session, redirect, url_for
from services.game_service import GameService
from config import DIFFICULTIES

app = Flask(__name__)
app.secret_key = "secret-key"

@app.route("/")
def index():
    session.pop("game", None)
    session.pop("result", None)
    
    return render_template(
        "index.html",
        state="start",
        difficulties=DIFFICULTIES
    )

#COMPLETED
@app.route("/start", methods=["POST"])
def start():
    difficulty = request.form["difficulty"]
    session["difficulty"] = difficulty

    game = GameService.create_game(difficulty)
    session["game"] = game.serialize()

    return render_template(
        "play.html",
        game=game,
        min_number=game.min_number,
        max_number=game.max_number,
        attempts_left=game.max_attempts,
        result=None
    )

#COMPLETED
@app.route("/guess", methods=["POST"])
def guess():
    if "game" not in session:
        return redirect(url_for("index"))

    game = GameService.restore_game(session["game"])
    result = GameService.process_guess(game, int(request.form["guess"]))

    session["game"] = game.serialize()

    if result["status"] in ["won", "lost"]:
        session["result"] = result
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

    game = GameService.restore_game(session["game"])
    result = session.get("result", None)

    return render_template(
        "end.html",
        result=result,
        game=game,
        won=(game.last_result == "won"),
        secret_number=game.secret_number,
        attempts=game.attempts
    )
    
#COMPLETED    
@app.route("/restart", methods=["POST"])
def restart():
    if "difficulty" not in session:
        return redirect(url_for("index"))
    
    difficulty = session["difficulty"]

    game = GameService.create_game(difficulty)

    session["game"] = game.serialize()
    session.pop("result", None)

    return render_template(
        "play.html",
        game=game,
        min_number=game.min_number,
        max_number=game.max_number,
        attempts_left=game.max_attempts,
        result=None
    )

@app.route("/exit", methods=["POST"])
def exit_game():
    session.clear()
    return render_template("goodbye.html")

if __name__ == "__main__":
    app.run(debug=True)