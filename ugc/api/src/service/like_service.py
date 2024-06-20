from sqlalchemy.orm import Session

from ugc.api.src.repository.like_repository import LikeSQLAlchemyRepository


class LikeService(LikeSQLAlchemyRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
