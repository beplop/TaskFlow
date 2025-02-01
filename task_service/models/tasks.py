from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from task_service.db.db import Base
from task_service.models.users import UsersModel
from task_service.schemas.tasks import TaskSchema


class TaskModel(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey(UsersModel.id), nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    assignee_id: Mapped[int] = mapped_column(ForeignKey(UsersModel.id), nullable=True)

    def to_read_model(self) -> TaskSchema:
        return TaskSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            author_id=self.author_id,
            assignee_id=self.assignee_id,
        )
