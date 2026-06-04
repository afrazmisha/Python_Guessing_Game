from flask import Flask, render_template, request, session, redirect, url_for
from services.game_service import GameService
from config import DIFFICULTIES

from models import db, GameState

app = Flask(__name__)
app.secret_key = "secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

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

    state = GameState(
        min_number=game.min_number,
        max_number=game.max_number,
        max_attempts=game.max_attempts,
        secret_number=game.secret_number,
        attempts=game.attempts,
        game_over=game.game_over,
        last_result=game.last_result,
        difficulty=difficulty
    )

    db.session.add(state)
    db.session.commit()

    session["game_id"] = state.id

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
    if "game_id" not in session:
        return redirect(url_for("index"))
    
    state = GameState.query.get(session["game_id"])

    if not state:
        return redirect(url_for("index"))

    game = GameService.game_from_state(state)

    result = GameService.process_guess(
        game,
        int(request.form["guess"])
    )

    GameService.update_state_from_game(state, game)
    db.session.commit()

    if result["status"] in ["won", "lost"]:
        return redirect(url_for("end"))

    return render_template(
        "play.html",
        game=game,
        min_number=game.min_number,
        max_number=game.max_number,
        attempts_left=game.max_attempts - game.attempts,
        result=result
    )

#COMPLETED
@app.route("/end")
def end():
    if "game_id" not in session:
        return redirect(url_for("index"))
    
    state = GameState.query.get(session["game_id"])

    if not state:
        return redirect(url_for("index"))

    game = GameService.game_from_state(state)
    
    return render_template(
        "end.html",
        result={
            "status": game.last_result,
            "message": "Correct!" if game.last_result == "won" else "Game Over!"
        },
        game=game,
        won=(game.last_result == "won"),
        secret_number=game.secret_number,
        attempts=game.attempts
    )
    
#COMPLETED    
@app.route("/restart", methods=["POST"])
def restart():
    if "game_id" not in session:
        return redirect(url_for("index"))
    
    state = GameState.query.get(session["game_id"])

    if not state:
        return redirect(url_for("index"))
    
    difficulty = state.difficulty

    game = GameService.create_game(difficulty)

    new_state = GameState(
        min_number=game.min_number,
        max_number=game.max_number,
        max_attempts=game.max_attempts,
        secret_number=game.secret_number,
        attempts=game.attempts,
        game_over=game.game_over,
        last_result=game.last_result,
        difficulty=difficulty
    )

    db.session.add(new_state)
    db.session.commit()

    session["game_id"] = new_state.id

    return render_template(
        "play.html",
        game=game,
        min_number=game.min_number,
        max_number=game.max_number,
        attempts_left=game.max_attempts,
        result=None
    )

@app.route("/history")
def history():
    games = GameState.query.order_by(GameState.id.desc()).all()

    return render_template(
        "history.html",
        games=games
    )

@app.route("/exit", methods=["POST"])
def exit_game():
    session.clear()
    return render_template("goodbye.html")

if __name__ == "__main__":
    app.run(debug=True)