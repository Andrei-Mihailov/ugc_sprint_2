from sqlalchemy.orm import Session

from ugc.api.src.models.bookmark import Bookmark


class BookmarkSQLAlchemyRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def find_all(self):
        return self.db.query(Bookmark).all()
