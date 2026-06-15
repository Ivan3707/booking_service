from typing import Generic, TypeVar, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")

class AbstractRepository(Generic[T]):
    """
    Базовый репозиторий с готовой логикой.
    Сюда стекаются общие методы для всех таблиц.
    """
    # Этот атрибут мы будем переопределять в дочерних классах (например, model = Room)
    model = None 

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> T | None:
        """Автоматический поиск по ID для любой модели."""
        if self.model is None:
            raise NotImplementedError("Необходимо указать атрибут model в дочернем классе")
        return await self.session.get(self.model, id)

    async def get_all(self) -> List[T]:
        """Автоматическое получение всех записей для любой модели."""
        if self.model is None:
            raise NotImplementedError("Необходимо указать атрибут model в дочернем классе")
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def create(self, **data) -> T:
        if self.model is None:
            raise NotImplementedError("model not set")

        obj = self.model(**data)
        self.session.add(obj)
        await self.session.flush()
        return obj
    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
    