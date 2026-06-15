from uuid import UUID
from sqlalchemy import  select
from sqlalchemy.dialects.postgresql import insert
from src.models.models import Schedule
from src.repositories.base import AbstractRepository

class ScheduleRepository(AbstractRepository[Schedule]):
    """Репозиторий для работы с правилами расписания комнат."""

    model = Schedule

    async def get_by_room_and_day(self, room_id: UUID, day_of_week: int) -> Schedule | None:
        """Ищет расписание для конкретной комнаты в определенный день недели."""
        query = select(Schedule).where(
            Schedule.room_id == room_id,
            Schedule.day_of_week == day_of_week
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_day(self, day_of_week: int) -> list[Schedule]:
        """Выгребает расписания ВСЕХ комнат для конкретного дня недели (нужно для робота)."""
        query = select(Schedule).where(Schedule.day_of_week == day_of_week)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, room_id: UUID, day_of_week: int, start_time, end_time) -> Schedule:
        """Создает новое правило расписания."""
        schedule = Schedule(
            room_id=room_id, 
            day_of_week=day_of_week, 
            start_time=start_time, 
            end_time=end_time
        )
        self.session.add(schedule)
        await self.session.flush()
        return schedule
    
    async def get_by_room_and_day(self, room_id, day_of_week):
        stmt = select(self.model).where(
            self.model.room_id == room_id,
            self.model.day_of_week == day_of_week
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    
    async def create(self, room_id, day_of_week, start_time, end_time):
        stmt = insert(Schedule).values(
            room_id=room_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time
        ).on_conflict_do_nothing(
            index_elements=["room_id", "day_of_week"]
        ).returning(Schedule)

        result = await self.session.execute(stmt)
        schedule = result.scalar_one_or_none()

        if schedule:
            return schedule

        # если уже создано другим потоком
        return await self.get_by_room_and_day(room_id, day_of_week)