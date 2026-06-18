from uuid import UUID
from datetime import datetime
from sqlalchemy import select, and_, text
from src.core.exceptions import BookingAlreadyExistsException, BookingNotFoundException, NotFoundException, PermissionDeniedException
from src.models.models import Booking, Slot, BookingStatusEnum
from src.repositories.base import AbstractRepository

class BookingRepository(AbstractRepository[Booking]):
    model = Booking

    async def cancel(self, booking_id: UUID):
        booking = await self.get_by_id(booking_id)

        if not booking:
            raise BookingNotFoundException()

        booking.status = BookingStatusEnum.CANCELLED

        return booking

    async def get_future_bookings(self, user_id: UUID) -> list[Booking]:
        """Фильтрация: только брони на будущие слоты."""
        query = (
            select(Booking)
            .join(Slot)
            .where(
                Booking.user_id == user_id,
                Booking.status == BookingStatusEnum.ACTIVE,
                Slot.start_at > datetime.utcnow()
            )
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def is_slot_busy(self, slot_id: UUID):
        result = await self.session.execute(
            select(Booking).where(
                Booking.slot_id == slot_id,
                Booking.status == BookingStatusEnum.ACTIVE
            )
        )
        return result.scalar_one_or_none() is not None
    
    async def create_booking(self, uow, schema):
        slot = await uow.slots.get_by_id(schema.slot_id)

        if not slot:
            raise NotFoundException("Slot not found")

        existing = await uow.bookings.get_active_by_slot(schema.slot_id)
        if existing:
            raise BookingAlreadyExistsException()

        booking = await uow.bookings.create(
            slot_id=schema.slot_id,
            user_id=schema.user_id,
            status="ACTIVE"
        )

        return booking
    
    async def get_my_bookings(self, uow, user_id):
        return await uow.bookings.get_by_user(user_id)
    
    async def get_by_user(self, user_id: UUID):
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()