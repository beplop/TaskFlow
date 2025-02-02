from sqlalchemy.orm import Mapped, mapped_column

from auth_service.db.db import Base
from auth_service.schemas.users import UserSchema


class UsersModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            name=self.name,
            password=self.password,
        )
