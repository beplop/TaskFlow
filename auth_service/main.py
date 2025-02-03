from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import datetime
from auth_service.db.redis import redis
import jwt

from auth_service.auth.auth import AuthService
# from auth_service.models.tokens import TokensModel
from auth_service.models.users import UsersModel
from auth_service.db.db import async_session_maker
from sqlalchemy import insert, select
from fastapi import APIRouter
from auth_service.db.db import (create_tables, delete_tables, #get_async_session,
                                async_session_maker)
from auth_service.schemas.tokens import TokenSchema, RefreshTokenSchema

from auth_service.schemas.users import UserSchema, UserSchemaAdd

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


# @router.post("/login")
# async def login(user: UserSchemaAdd):
#     async with async_session_maker() as session:
#         stmt = select(UsersModel).where(UsersModel.name == user.name)
#         result = await session.execute(stmt)
#         user_record = result.scalar_one_or_none()
#         if user_record and user_record.password == user.password:
#             return {"token": create_token(user.username)}
#     raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/login", response_model=TokenSchema)
async def login(user: UserSchemaAdd):
    async with async_session_maker() as session:
        result = await session.execute(select(UsersModel).where(UsersModel.name == user.name))
        db_user = result.scalar_one_or_none()
        if not db_user or not AuthService.verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = await AuthService.create_access_token(data={"sub": db_user.username})
        refresh_token = await AuthService.create_refresh_token(data={"sub": db_user.username})

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(username: str):
    await AuthService.revoke_token(username)
    return {"message": "Logged out successfully"}


@router.post("/refresh", response_model=TokenSchema)
async def refresh_token(refresh_data: RefreshTokenSchema):
    token = refresh_data.refresh_token
    ALGORITHM = "HS256"
    SECRET_KEY = "supersecret"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        redis_token = await redis.get(f"refresh_token:{username}")
        if redis_token != token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Генерируем новый access-токен
        new_access_token = await AuthService.create_access_token(data={"sub": username})

        return {"access_token": new_access_token, "refresh_token": token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")


@router.post("/register", response_model=TokenSchema)
async def register(user: UserSchemaAdd):
    async with async_session_maker() as session:
        result = await session.execute(select(UsersModel).where(UsersModel.name == user.name))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = AuthService.hash_password(user.password)
        new_user = UsersModel(name=user.name, password=hashed_password)
        session.add(new_user)
        await session.commit()

        access_token = await AuthService.create_access_token(data={"sub": user.name})
        refresh_token = await AuthService.create_refresh_token(data={"sub": user.name})

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# @router.get("/verify")
# def verify_token(token: str):
#     try:
#         decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return {"username": decoded["sub"]}
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")

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