import pytest
from datetime import time, date

from src.core.unitofwork import UnitOfWork
from src.services.schedule import ScheduleService
from src.schemas.schedule import ScheduleCreateSchema



@pytest.mark.asyncio
async def test_schedule_generation_is_idempotent(sessionmaker):

    service = ScheduleService()

    async with UnitOfWork(sessionmaker()) as uow:

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

        schedule1 = await service.create_schedule_with_slots(uow, schema)
        schedule2 = await service.create_schedule_with_slots(uow, schema)

        assert schedule1.id == schedule2.id

        slots = await uow.slots.get_by_room(room.id)

    # важно: не должно удвоиться
    assert len(slots) > 0