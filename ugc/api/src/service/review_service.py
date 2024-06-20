from sqlalchemy.orm import Session

from ugc.api.src.repository.review_repository import ReviewSQLAlchemyRepository


class ReviewService(ReviewSQLAlchemyRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
