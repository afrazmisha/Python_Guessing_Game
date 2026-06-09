from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from services.game_service import GameService
from config import DIFFICULTIES
from models import db, GameState, User
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret-key"

app.permanent_session_lifetime = timedelta(minutes=10)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    session.pop("game", None)
    session.pop("result", None)
    
    return render_template(
        "index.html",
        state="start",
        difficulties=DIFFICULTIES,
        username=session.get("username")
    )

#COMPLETED
@app.route("/start", methods=["POST"])
def start():
    if "user_id" not in session:
        return redirect(url_for("login"))

    difficulty = request.form["difficulty"]
    session["difficulty"] = difficulty

    game = GameService.create_game(difficulty)

    state = GameState(
        user_id=session.get("user_id"),
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
    if "user_id" not in session:
        return redirect(url_for("login"))
    
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
    if "user_id" not in session:
        return redirect(url_for("login"))
    
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
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if "game_id" not in session:
        return redirect(url_for("index"))
    
    state = GameState.query.get(session["game_id"])

    if not state:
        return redirect(url_for("index"))
    
    difficulty = state.difficulty

    game = GameService.create_game(difficulty)

    new_state = GameState(
        user_id=session.get("user_id"),
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
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if "user_id" not in session:
        return redirect(url_for("login"))

    games = GameState.query.filter_by(
        user_id=session["user_id"]
    ).order_by(GameState.id.desc()).all()

    return render_template(
        "history.html",
        games=games
    )

@app.route("/stats")
def stats():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    total_games = GameState.query.filter_by(user_id=user_id).count()
    wins = GameState.query.filter_by(user_id=user_id, last_result="won").count()
    losses = GameState.query.filter_by(user_id=user_id, last_result="lost").count()
    in_progress = GameState.query.filter_by(user_id=user_id, game_over=False).count()

    completed_games = wins + losses

    win_rate = 0
    if completed_games > 0:
        win_rate = (wins / completed_games) * 100

    completed_attempts = GameState.query.filter_by(
        user_id=user_id,
        game_over=True
    ).all()

    average_attempts = 0
    if completed_attempts:
        total_attempts = sum(game.attempts for game in completed_attempts)
        average_attempts = total_attempts / len(completed_attempts)

    best_game = GameState.query.filter_by(
        user_id=user_id,
        last_result="won"
    ).order_by(GameState.attempts.asc()).first()

    return render_template(
        "stats.html",
        total_games=total_games,
        wins=wins,
        losses=losses,
        in_progress=in_progress,
        win_rate=win_rate,
        average_attempts=average_attempts,
        best_game=best_game
    )

@app.route("/exit", methods=["POST"])
def exit_game():
    session.clear()
    return render_template("goodbye.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "Username already exists"

        password_hash = generate_password_hash(password)

        user = User(
            username=username,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            return "Invalid username or password"

        if not check_password_hash(user.password_hash, password):
            return "Invalid username or password"

        session.permanent = True
        session["user_id"] = user.id
        session["username"] = user.username

        return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)