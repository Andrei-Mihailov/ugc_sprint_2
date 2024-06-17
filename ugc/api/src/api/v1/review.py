from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from ugc.api.src.main import app, db
from models.review import Review


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reviews.db"

ugc_blueprint = Blueprint("ugc", __name__, url_prefix="/ugc")

db.create_all()


@ugc_blueprint.route("/api/v1/<movie_id>/review", methods=["GET", "POST"])
def add_review(movie_id):
    user_id = get_jwt_identity()
    review = request.get_json()
    review = Review(movie_id=movie_id, user_id=user_id, **review)
    db.session.add(review)
    db.session.commit()
    return "", 200


@ugc_blueprint.route("/api/v1/<movie_id>/review", methods=["GET", "POST"])
def retrieve_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200


@ugc_blueprint.route("/api/v1/<movie_id>/review", methods=["GET", "POST"])
def delete_review(movie_id):
    user_id = get_jwt_identity()
    review = request.get_json()
    review = Review.query.filter_by(
        movie_id=movie_id, user_id=user_id, **review
    ).first()
    if review is not None:
        db.session.delete(review)
        db.session.commit()
    return "", 200
