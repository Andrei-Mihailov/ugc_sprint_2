from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.review import Review
from sentry_sdk import capture_message

from ugc.api.src.main import app, db

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reviews.db"

ugc_blueprint = Blueprint("ugc", __name__, url_prefix="/ugc")

db.create_all()


@ugc_blueprint.route("/api/v1/<movie_id>/review", methods=["GET", "POST"])
@jwt_required
def add_review(movie_id):
    user_id = get_jwt_identity()
    review = request.get_json()
    review = Review(movie_id=movie_id, user_id=user_id, **review)
    db.session.add(review)
    db.session.commit()
    capture_message(f"User {user_id} added review for movie {movie_id}")
    return "", 200


@ugc_blueprint.route("/api/v1/<int:movie_id>/reviews", methods=["GET"])
@jwt_required
def retrieve_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    capture_message(f"Retrieved reviews for movie {movie_id}")
    return jsonify([review.to_dict() for review in reviews]), 200


@ugc_blueprint.route("/api/v1/<movie_id>/review", methods=["GET", "POST"])
@jwt_required
def delete_review(movie_id):
    user_id = get_jwt_identity()
    review = request.get_json()
    review = Review.query.filter_by(movie_id=movie_id, user_id=user_id, **review).first()
    if review is not None:
        db.session.delete(review)
        db.session.commit()
        capture_message(f"User {user_id} deleted review for movie {movie_id}")
        return "", 200
    else:
        capture_message(f"Review not found for user {user_id} and movie {movie_id}")
        return jsonify({"error": "Review not found"}), 404
