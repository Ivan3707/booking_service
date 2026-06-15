from uuid import UUID

from sqlalchemy import text

from src.core.database import async_session_maker
from src.repositories.room import RoomRepository
from src.repositories.schedule import ScheduleRepository
from src.repositories.slot import SlotRepository
from src.repositories.booking import BookingRepository
from src.repositories.user import UsersRepository

class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        # Инициализируем каждый репозиторий своей зоной ответственности
        self.rooms = RoomRepository(self.session)
        self.schedules = ScheduleRepository(self.session)
        self.slots = SlotRepository(self.session)
        self.bookings = BookingRepository(self.session)
        self.users = UsersRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()