from uuid import UUID
from sqlalchemy import  select
from sqlalchemy.dialects.postgresql import insert
from src.models.models import Schedule
from src.repositories.base import AbstractRepository

class ScheduleRepository(AbstractRepository[Schedule]):
    """Репозиторий для работы с правилами расписания комнат."""

    model = Schedule

    async def get_by_day(self, day_of_week: int) -> list[Schedule]:
        """Выгребает расписания ВСЕХ комнат для конкретного дня недели (нужно для робота)."""
        query = select(Schedule).where(Schedule.day_of_week == day_of_week)
        result = await self.session.execute(query)
        return list(result.scalars().all())

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
    

    async def get_by_room(self, room_id: UUID):
        stmt = select(self.model).where(self.model.room_id == room_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()