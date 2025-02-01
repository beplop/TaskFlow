from fastapi import APIRouter

from task_service.schemas.tasks import TaskSchemaAdd
from task_service.services.tasks import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("")
async def list_tasks() -> list[TaskSchemaAdd]:
    tasks = await TaskService().get_all()
    return tasks


@router.post("")
async def add_task(task: TaskSchemaAdd) -> dict:
    task_id = await TaskService().add(task)
    return {'task_id': task_id}
