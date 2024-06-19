from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.like import Like
from sentry_sdk import capture_message

from ugc.api.src.main import app, db

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///likes.db"


ugc_blueprint = Blueprint("ugc", __name__, url_prefix="/ugc")

db.create_all()


@ugc_blueprint.route("/api/v1/<movie_id>/like", methods=["GET", "POST"])
@jwt_required
def add_like(movie_id):
    user_id = get_jwt_identity()
    like = Like.query.filter_by(movie_id=movie_id, user_id=user_id).first()
    if like is None:
        like = Like(movie_id=movie_id, user_id=user_id)
        db.session.add(like)
        db.session.commit()
        capture_message(f"User {user_id} liked movie {movie_id} for the first time")
    else:
        like.like += 1
        db.session.commit()
        capture_message(f"User {user_id} liked movie {movie_id} again")
    return "", 200


@ugc_blueprint.route("/api/v1/<movie_id>/dislike", methods=["GET", "POST"])
@jwt_required
def add_dislike(movie_id):
    user_id = get_jwt_identity()
    like = Like.query.filter_by(movie_id=movie_id, user_id=user_id).first()
    if like is None:
        like = Like(movie_id=movie_id, user_id=user_id)
        db.session.add(like)
        db.session.commit()
        capture_message(f"User {user_id} disliked movie {movie_id} for the first time")
    else:
        like.dislike += 1
        db.session.commit()
        capture_message(f"User {user_id} disliked movie {movie_id} again")
    return "", 200
