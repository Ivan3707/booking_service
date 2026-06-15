from uuid import UUID
from datetime import date, datetime, time
from sqlalchemy.dialects.postgresql  import insert as pg_insert
from sqlalchemy import select, and_
from src.models.models import Slot, Booking, BookingStatusEnum
from src.repositories.base import AbstractRepository

class SlotRepository(AbstractRepository[Slot]):
    model = Slot

    async def get_available_slots(self, room_id: UUID, target_date: date) -> list[Slot]:
        """Ищет слоты, которые не заняты активной бронью."""
        day_start = datetime.combine(target_date, time.min)
        day_end = datetime.combine(target_date, time.max)

        query = (
            select(Slot)
            .outerjoin(Booking, and_(
                Booking.slot_id == Slot.id,
                Booking.status == BookingStatusEnum.ACTIVE
            ))
            .where(
                Slot.room_id == room_id,
                Slot.start_at >= day_start,
                Slot.start_at <= day_end,
                Booking.id == None 
            )
            .order_by(Slot.start_at)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    
    async def add_bulk_safe(self, slots: list):
        if not slots:
            return

        clean_slots = []
        for s in slots:
            clean_slots.append({
                "room_id": s.room_id,
                "start_at": s.start_at,
                "end_at": s.end_at,
            })

        stmt = pg_insert(self.model).values(clean_slots)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["room_id", "start_at"]
        )

        await self.session.execute(stmt)

    async def get_by_room(self, room_id):
        stmt = select(self.model).where(self.model.room_id == room_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()