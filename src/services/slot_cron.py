from datetime import UTC, datetime, timedelta
from src.core.unitofwork import UnitOfWork
from src.domain.slot_generator import DomainSlotGenerator

class SlotCronService:
    """Сервис для фоновых задач (Cron) по обслуживанию тайм-слотов."""

    async def cron_daily_pregenerate_slots(self, uow: UnitOfWork):
        """Каждую ночь подготавливает «хвост» слотов на 30-й день вперед."""
        target_date =  datetime.now(UTC).date()  + timedelta(days=30)
        
        schedules = await uow.schedules.get_by_day(target_date.weekday())
        
        for schedule in schedules:
            generated_slots = DomainSlotGenerator.generate_intervals(
                room_id=schedule.room_id,
                target_date=target_date,
                start_time=schedule.start_time,
                end_time=schedule.end_time
            )
            await uow.slots.add_bulk_safe(generated_slots)
            
        print(f"🤖 [CRON] Высокоэффективная генерация слотов завершена на {target_date}")