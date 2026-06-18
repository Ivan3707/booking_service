import pytest
from datetime import datetime, timedelta

from src.core.unitofwork import UnitOfWork
from src.schemas.booking import BookingCreateSchema
from src.services.booking import BookingService
from src.core.exceptions import BadRequestException


@pytest.mark.asyncio
async def test_create_booking_past_slot(sessionmaker):

    service = BookingService()

    async with UnitOfWork(sessionmaker) as uow:

        user = await uow.users.create(
            email="past@test.com"
        )

        room = await uow.rooms.create(
            name="Room",
            description="test",
            capacity=10
        )

        slot = await uow.slots.create(
            room_id=room.id,
            start_at=datetime.utcnow() - timedelta(hours=2),
            end_at=datetime.utcnow() - timedelta(hours=1)
        )

    async with UnitOfWork(sessionmaker) as uow:

        with pytest.raises(BadRequestException):

            await service.create_booking(
                uow,
                BookingCreateSchema(slot_id=slot.id),
                user_id=user.id
            )