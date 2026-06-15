from uuid import UUID
from datetime import datetime
from sqlalchemy import select, and_, text
from src.core.exceptions import BookingNotFoundException, PermissionDeniedException
from src.models.models import Booking, Slot, BookingStatusEnum
from src.repositories.base import AbstractRepository

class BookingRepository(AbstractRepository[Booking]):
    model = Booking

    async def cancel_booking(self, booking_id: UUID, user_id: UUID) -> Booking:
        """Отмена брони с идемпотентностью (смена статуса, а не delete)."""
        booking = await self.get_by_id(booking_id)
        if not booking:
            raise BookingNotFoundException()

        if booking.user_id != user_id:
            raise PermissionDeniedException()

        # Идемпотентность: если уже cancelled, ничего не делаем
        if booking.status == BookingStatusEnum.CANCELLED:
            return booking
            
        booking.status = BookingStatusEnum.CANCELLED
        # await self.session.flush() # Не обязательно, UOW сам сделает commit
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