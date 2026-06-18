import pytest
from datetime import datetime, timedelta

from src.core.unitofwork import UnitOfWork
from src.schemas.booking import BookingCreateSchema
from src.services.booking import BookingService
from src.models.models import BookingStatusEnum


@pytest.mark.asyncio
async def test_cancel_booking_success(sessionmaker):

    service = BookingService()

    async with UnitOfWork(sessionmaker) as uow:

        user = await uow.users.create(
            email="cancel@test.com"
        )

        room = await uow.rooms.create(
            name="Room",
            description="test",
            capacity=10
        )

        slot = await uow.slots.create(
            room_id=room.id,
            start_at=datetime.utcnow() + timedelta(hours=1),
            end_at=datetime.utcnow() + timedelta(hours=2)
        )

    async with UnitOfWork(sessionmaker) as uow:

        booking = await service.create_booking(
            uow,
            BookingCreateSchema(slot_id=slot.id),
            user_id=user.id
        )

    async with UnitOfWork(sessionmaker) as uow:

        result = await service.cancel_booking(
            uow,
            booking.id
        )

    assert result.status == BookingStatusEnum.CANCELLED