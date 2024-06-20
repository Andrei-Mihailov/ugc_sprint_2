from models.bookmark import Bookmark
from sqlalchemy.orm import Session


class BookmarkSQLAlchemyRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def find_all(self):
        return self.db.query(Bookmark).all()
