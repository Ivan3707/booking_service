import pytest
from datetime import time

from src.repositories.unitofwork import UnitOfWork
from src.services.schedule import ScheduleService
from src.schemas.schedule import ScheduleCreateSchema


@pytest.mark.asyncio
async def test_schedule_unique_constraint():
    service = ScheduleService()

    async with UnitOfWork() as uow:
        room = await uow.rooms.create(
            name="Room",
            description="test",
            capacity=10
        )

    schema = ScheduleCreateSchema(
        room_id=room.id,
        day_of_week=1,
        start_time=time(9, 0),
        end_time=time(10, 0)
    )

    # первый успешный
    async with UnitOfWork() as uow:
        await service.create_schedule_with_slots(uow, schema)

    # второй должен упасть
    with pytest.raises(Exception):
        async with UnitOfWork() as uow:
            await service.create_schedule_with_slots(uow, schema)