from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///likes.db'
db = SQLAlchemy(app)

jwt = JWTManager(app)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.String(128), nullable=False)
    like = db.Column(db.Integer, default=0)
    dislike = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Like movie_id={self.movie_id}, user_id={self.user_id}, like={self.like}, dislike={self.dislike}>"


db.create_all()


@jwt_required()
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
    return '', 200


@jwt_required()
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
    return '', 200


api.add_resource(add_like, '/api/v1/<movie_id>/like')
api.add_resource(add_dislike, '/api/v1/<movie_id>/dislike')

