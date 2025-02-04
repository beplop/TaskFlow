from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from auth_service.db.redis import redis
from auth_service.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def create_access_token(data: dict):
        expire = datetime.utcnow() + timedelta(minutes=settings.auth_jwt.access_token_expire_minutes)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode,
                           settings.auth_jwt.private_key_path.read_text(),
                           algorithm=settings.auth_jwt.algorithm)

        await redis.setex(f"access_token:{data['sub']}", settings.auth_jwt.access_token_expire_minutes * 60, token)

        return token

    @staticmethod
    async def create_refresh_token(data: dict):
        expire = datetime.utcnow() + timedelta(days=settings.auth_jwt.refresh_token_expire_days)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, settings.auth_jwt.private_key_path.read_text(),
                           algorithm=settings.auth_jwt.algorithm)

        await redis.setex(f"refresh_token:{data['sub']}", settings.auth_jwt.refresh_token_expire_days * 86400, token)

        return token

    @staticmethod
    async def revoke_token(username: str):
        """Удаляет токены пользователя из Redis"""
        await redis.delete(f"access_token:{username}")
        await redis.delete(f"refresh_token:{username}")

    @staticmethod
    async def get_token_from_redis(username: str):
        """Получает токен из Redis"""
        return await redis.get(f"access_token:{username}")
