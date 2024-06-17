from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound

from core import security_jwt_remote
from services import BookmarkService, get_bookmark_service

blueprint = Blueprint("bookmark", __name__, url_prefix="/api/v1")


@blueprint.route("/<movie_id>/bookmark", methods=["POST"])
@jwt_required
def add_bookmark(movie_id: int):
    user_id = get_jwt_identity()

    bookmark_service = get_bookmark_service()
    bookmark_service.create({"movie_id": movie_id, "user_id": user_id})

    return jsonify({"success": True}), 200


@blueprint.route("/<movie_id>/bookmark", methods=["DELETE"])
@jwt_required
def delete_bookmark(movie_id: int):
    user_id = get_jwt_identity()

    bookmark_service = get_bookmark_service()
    bookmark = bookmark_service.get_by_movie_id_and_user_id(movie_id, user_id)

    if not bookmark:
        raise NotFound(description="Bookmark not found")

    bookmark_service.delete(bookmark)

    return (jsonify({"success": True}),)
