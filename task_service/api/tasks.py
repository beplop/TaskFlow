import httpx
from fastapi import APIRouter

from task_service.schemas.tasks import TaskSchemaAdd, UserSchema
from task_service.services.tasks import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

AUTH_SERVICE_URL = "http://127.0.0.1:8003/auth"


@router.get("/")
async def list_tasks() -> list[TaskSchemaAdd]:
    tasks = await TaskService().get_all()
    return tasks


@router.post("/")
async def add_task(task: TaskSchemaAdd) -> dict:
    task_id = await TaskService().add(task)
    return {'task_id': task_id}


@router.get("/get_users")
async def get_users() -> list[UserSchema]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTH_SERVICE_URL}/send_user")
        return response.json()
