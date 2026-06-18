from src.core.database import async_session_maker
from src.core.unitofwork import UnitOfWork

async def get_uow():
    async with async_session_maker() as session:
        async with UnitOfWork(session) as uow:
            yield uow