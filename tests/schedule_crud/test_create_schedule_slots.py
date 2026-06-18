import pytest
from datetime import time, date

from src.core.unitofwork import UnitOfWork
from src.services.schedule import ScheduleService
from src.schemas.schedule import ScheduleCreateSchema


@pytest.mark.asyncio
async def test_create_schedule_creates_slots(sessionmaker):

    service = ScheduleService()

    async with UnitOfWork(sessionmaker) as uow:

        room = await uow.rooms.create(
            name="Test Room",
            description="test",
            capacity=10
        )

        schema = ScheduleCreateSchema(
            room_id=room.id,
            day_of_week=date.today().weekday(),
            start_time=time(9, 0),
            end_time=time(10, 0)
        )

        schedule = await service.create_schedule_with_slots(uow, schema)

        slots = await uow.slots.get_by_room(room.id)

    assert schedule.id is not None
    assert len(slots) > 0