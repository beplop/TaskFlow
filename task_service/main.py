from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from task_service.api.tasks import router
from sqlalchemy import select
from task_service.db.db import (create_tables, delete_tables, #get_async_session,
                                async_session_maker)
from task_service.models.users import UsersModel


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # await delete_tables()
#     # print("База очищена")
#     await create_tables()
#     print("Base created")
#     yield
#     print("Off")

app = FastAPI(#lifespan=lifespan,
              title='Сервис управления задачами')
app.include_router(router)


# @app.get("/")
# async def get_users():
#     async with async_session_maker() as session:
#         query = select(UsersModel)
#         result = await session.execute(query)
#         users = result.scalars().all()  # Извлечение всех результатов
#         return [{"id": user.id, "name": user.name} for user in users]
