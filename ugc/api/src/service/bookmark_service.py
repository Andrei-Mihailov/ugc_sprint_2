from db import get_mongo
from flask import g
from motor.motor_asyncio import AsyncIOMotorClient
from repositories import MongoRepository


class BookmarkService(MongoRepository):
    def __init__(self, mongo: AsyncIOMotorClient) -> None:
        super().__init__(mongo, 'bookmarks')


def get_bookmark_service() -> BookmarkService:
    mongo = get_mongo()
    return BookmarkService(mongo)


def before_request():
    g.bookmark_service = get_bookmark_service()


async def get_bookmarks():
    bookmarks = await g.bookmark_service.find_all()
    return {"bookmarks": bookmarks}
