from task_service.db.db import async_session_maker #get_async_session
from fastapi import Depends
from task_service.repositories.tasks import TaskRepository


class TaskService:
    @staticmethod
    async def add(task):
        async with async_session_maker() as session:
            task_dict = task.model_dump()
            task_id = await TaskRepository(session).add(task_dict)
            await session.commit()
            return task_id

    @staticmethod
    async def get_all():
        async with async_session_maker() as session:
            tasks = await TaskRepository(session).get_all()
            return tasks
