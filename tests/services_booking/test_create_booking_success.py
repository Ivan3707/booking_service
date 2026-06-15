import pytest
from uuid import uuid4
from datetime import datetime, timedelta

from src.repositories.unitofwork import UnitOfWork
from src.schemas.booking import BookingCreateSchema
from src.services.booking import BookingService


@pytest.mark.asyncio
async def test_create_booking_success():

    service = BookingService()

    async with UnitOfWork() as uow:

        user = await uow.users.create(
            email="test@test.com"
        )

        room = await uow.rooms.create(
            name="Test Room",
            description="test",
            capacity=10
        )

        slot = await uow.slots.create(
            room_id=room.id,
            start_at=datetime.now() + timedelta(minutes=10),
            end_at=datetime.now() + timedelta(hours=1)
        )

    async with UnitOfWork() as uow:

        booking = await service.create_booking(
            uow,
            BookingCreateSchema(slot_id=slot.id),
            user_id=user.id
        )

    assert booking is not None
    assert booking.slot_id == slot.id
    assert booking.user_id == user.id