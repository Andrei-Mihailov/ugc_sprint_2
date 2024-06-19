from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.like import Like
from models.movie import Movie
from sentry_sdk import capture_message

from ugc.api.src.main import app, db

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///likes.db"

ugc_blueprint = Blueprint("ugc", __name__, url_prefix="/ugc")

db.create_all()


@ugc_blueprint.route("/api/v1/<movie_id>/like", methods=["POST"])
@jwt_required()
def add_like(movie_id):
    user_id = get_jwt_identity()
    like = Like.query.filter_by(movie_id=movie_id, user_id=user_id).first()
    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    if like is None:
        like = Like(movie_id=movie_id, user_id=user_id, is_like=True)
        db.session.add(like)
        movie.like_count += 1
        db.session.commit()
        capture_message(f"User {user_id} liked movie {movie_id} for the first time")
    else:
        if like.is_like:
            return jsonify({"message": "Already liked"}), 400
        else:
            like.is_like = True
            movie.like_count += 1
            movie.dislike_count -= 1
            db.session.commit()
            capture_message(f"User {user_id} changed dislike to like for movie {movie_id}")

    return "", 200


@ugc_blueprint.route("/api/v1/<movie_id>/dislike", methods=["POST"])
@jwt_required()
def add_dislike(movie_id):
    user_id = get_jwt_identity()
    like = Like.query.filter_by(movie_id=movie_id, user_id=user_id).first()
    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    if like is None:
        like = Like(movie_id=movie_id, user_id=user_id, is_like=False)
        db.session.add(like)
        movie.dislike_count += 1
        db.session.commit()
        capture_message(f"User {user_id} disliked movie {movie_id} for the first time")
    else:
        if not like.is_like:
            return jsonify({"message": "Already disliked"}), 400
        else:
            like.is_like = False
            movie.like_count -= 1
            movie.dislike_count += 1
            db.session.commit()
            capture_message(f"User {user_id} changed like to dislike for movie {movie_id}")

    return "", 200


@ugc_blueprint.route("/api/v1/<movie_id>/likes", methods=["GET"])
def get_likes(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify({"likes": movie.like_count, "dislikes": movie.dislike_count}), 200
