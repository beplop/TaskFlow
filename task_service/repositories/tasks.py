from task_service.models.tasks import TaskModel
from task_service.schemas.tasks import TaskSchema
from task_service.utils.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = TaskModel
    schema = TaskSchema
