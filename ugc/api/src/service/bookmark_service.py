from sqlalchemy.orm import Session

from ugc.api.src.repository.bookmark_repository import BookmarkSQLAlchemyRepository


class BookmarkService(BookmarkSQLAlchemyRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)


def get_bookmark_service(db: Session) -> BookmarkService:
    return BookmarkService(db)
