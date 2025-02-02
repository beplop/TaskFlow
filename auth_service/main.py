from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import jwt
import datetime
from auth_service.models.users import UsersModel
from auth_service.db.db import async_session_maker
from sqlalchemy import insert, select
from fastapi import APIRouter
from auth_service.db.db import (create_tables, delete_tables, #get_async_session,
                                async_session_maker)

from auth_service.schemas.users import UserSchema, UserSchemaAdd

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

SECRET_KEY = "supersecret"

@router.post("/login")
async def login(user: UserSchemaAdd):
    async with async_session_maker() as session:
        stmt = select(UsersModel).where(UsersModel.name == user.name)
        result = await session.execute(stmt)
        user_record = result.scalar_one_or_none()
        if user_record and user_record.password == user.password:
            return {"token": create_token(user.username)}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/")
async def index() -> dict:
    return {"hello": "hello"}

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@router.post("/register")
async def register(user: UserSchemaAdd):
    async with async_session_maker() as session:
        user_dict = user.model_dump()
        stmt = insert(UsersModel).values(**user_dict).returning(UsersModel.id)
        result = await session.execute(stmt)
        await session.commit()
        # return result.scalar_one()
    return {"username": user_dict['name']}

@router.get("/verify")
def verify_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"username": decoded["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/send_user")
async def send_user() -> list[UserSchema]:
    async with async_session_maker() as session:
        stmt = select(UsersModel)
        result = await session.execute(stmt)
        result_schemas = [UserSchema.model_validate(row[0]) for row in result.all()]
    return result_schemas

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await delete_tables()
#     print("База очищена")
#     await create_tables()
#     print("Base created")
#     yield
#     print("Off")

app = FastAPI()#lifespan=lifespan)
app.include_router(router)