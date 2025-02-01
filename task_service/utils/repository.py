from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    # @abstractmethod
    # def edit(self):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def delete(self):
    #     raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None
    schema = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_all(self) -> list:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        result_schemas = [self.schema.model_validate(row[0]) for row in result.all()]
        # result_schemas = [row[0].to_read_model() for row in result.all()]
        return result_schemas
