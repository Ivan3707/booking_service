from src.repositories.room import RoomRepository
from src.repositories.schedule import ScheduleRepository
from src.repositories.slot import SlotRepository
from src.repositories.booking import BookingRepository
from src.repositories.user import UsersRepository


class UnitOfWork:
    def __init__(self, session_source):
        self._session_source = session_source
        self.session = None

    async def __aenter__(self):
        # CASE 1: передали sessionmaker
        if hasattr(self._session_source, "__call__"):
            self.session = self._session_source()
        else:
            # CASE 2: передали уже session
            self.session = self._session_source

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