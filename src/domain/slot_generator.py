from datetime import datetime, date, timedelta, time
from uuid import UUID

from src.models.models import Slot

class DomainSlotGenerator:
    @staticmethod
    def generate_intervals(
        room_id: UUID,
        target_date: date,
        start_time: time,
        end_time: time
    ) -> list[Slot]:

        current = datetime.combine(target_date, start_time)
        final = datetime.combine(target_date, end_time)

        slots: list[Slot] = []

        while current + timedelta(minutes=30) <= final:
            slot_end = current + timedelta(minutes=30)

            slots.append(
                Slot(
                    room_id=room_id,
                    start_at=current,
                    end_at=slot_end
                )
            )

            current = slot_end

        return slots