from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
db = SQLAlchemy(app)

jwt = JWTManager(app)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.String(128), nullable=False)
    review = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f"<Review movie_id={self.movie_id}, user_id={self.user_id}, review={self.review}>"


db.create_all()


@jwt_required()
def add_review(movie_id):
    user_id = get_jwt_identity()
    review = request.get_json()
    review = Review(movie_id=movie_id, user_id=user_id, **review)
    db.session.add(review)
    db.session.commit()
    return '', 200


@jwt_required()
def retrieve_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200


@jwt_required()
def delete_review(movie_id):
    user_id = get_jwt_identity()
    review = request.get_json()
    review = Review.query.filter_by(movie_id=movie_id, user_id=user_id, **review).first()
    if review is not None:
        db.session.delete(review)
        db.session.commit()
    return '', 200


api.add_resource(add_review, '/api/v1/<movie_id>/review')
api.add_resource(retrieve_reviews, '/api/v1/<movie_id>/review')
api.add_resource(delete_review, '/api/v1/<movie_id>/review')

if __name__ == '__main__':
    app.run(debug=True)