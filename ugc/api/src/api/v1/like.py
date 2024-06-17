from flask import Flask, request, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from ugc.api.src.main import app, db
from models.like import Like


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
    else:
        like.like += 1
        db.session.commit()
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
    else:
        like.dislike += 1
        db.session.commit()
    return "", 200
