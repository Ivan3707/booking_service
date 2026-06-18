import pytest
from datetime import time, date

from src.core.unitofwork import UnitOfWork
from src.services.schedule import ScheduleService
from src.schemas.schedule import ScheduleCreateSchema
from src.core.exceptions import ScheduleAlreadyExistsException


@pytest.mark.asyncio
async def test_schedule_already_exists(sessionmaker):

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

    async with UnitOfWork(sessionmaker) as uow:
        await service.create_schedule_with_slots(uow, schema)

    async with UnitOfWork(sessionmaker) as uow:
        with pytest.raises(ScheduleAlreadyExistsException):
            await service.create_schedule_with_slots(uow, schema)