from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    min_number = db.Column(db.Integer, nullable=False)
    max_number = db.Column(db.Integer, nullable=False)
    max_attempts = db.Column(db.Integer, nullable=False)

    secret_number = db.Column(db.Integer, nullable=False)
    attempts = db.Column(db.Integer, default=0)

    game_over = db.Column(db.Boolean, default=False)
    last_result = db.Column(db.String(20))
    difficulty = db.Column(db.String(20))