from datetime import UTC, datetime, timedelta
from src.core.exceptions import ScheduleAlreadyExistsException
from src.domain.slot_generator import DomainSlotGenerator

class ScheduleService:
    """Сервис для управления расписанием комнат (административная панель)."""

    async def create_schedule_with_slots(self, uow, schema):
        schedule = await uow.schedules.get_by_room_and_day(
            schema.room_id,
            schema.day_of_week
        )

        if schedule:
            raise ScheduleAlreadyExistsException()

        schedule = await uow.schedules.create(
            room_id=schema.room_id,
            day_of_week=schema.day_of_week,
            start_time=schema.start_time,
            end_time=schema.end_time
)

        today = datetime.now(UTC).date()

        for i in range(30):
            d = today + timedelta(days=i)

            if d.weekday() != schema.day_of_week:
                continue

            slots = DomainSlotGenerator.generate_intervals(
                room_id=schema.room_id,
                target_date=d,
                start_time=schedule.start_time,
                end_time=schedule.end_time
            )

            await uow.slots.add_bulk_safe(slots)

        return schedule