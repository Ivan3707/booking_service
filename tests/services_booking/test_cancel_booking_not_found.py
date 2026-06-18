import pytest
from uuid import uuid4

from src.core.unitofwork import UnitOfWork
from src.schemas.booking import BookingCreateSchema
from src.services.booking import BookingService
from src.core.exceptions import SlotNotFoundException


@pytest.mark.asyncio
async def test_create_booking_slot_not_found(sessionmaker):

    service = BookingService()

    async with UnitOfWork(sessionmaker) as uow:
        with pytest.raises(SlotNotFoundException):
            await service.create_booking(
                uow,
                BookingCreateSchema(slot_id=uuid4()),
                user_id=uuid4()
            )