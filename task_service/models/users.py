from sqlalchemy.orm import Mapped, mapped_column

from task_service.db.db import Base


class UsersModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]