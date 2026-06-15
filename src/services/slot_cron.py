from datetime import date, timedelta
from src.repositories.unitofwork import UnitOfWork
from src.domain.slot_generator import DomainSlotGenerator

class SlotCronService:
    """Сервис для фоновых задач (Cron) по обслуживанию тайм-слотов."""

    async def cron_daily_pregenerate_slots(self, uow: UnitOfWork):
        """Каждую ночь подготавливает «хвост» слотов на 30-й день вперед."""
        async with uow:
            target_date = date.today() + timedelta(days=30)
            
            schedule_stream = uow.schedules.stream_by_day(target_date.weekday())
            
            async for schedule in schedule_stream:
                generated_slots = DomainSlotGenerator.generate_intervals(
                    room_id=schedule.room_id,
                    target_date=target_date,
                    start_time=schedule.start_time,
                    end_time=schedule.end_time
                )
                await uow.slots.add_bulk_safe(generated_slots)
                
            print(f"🤖 [CRON] Высокоэффективная генерация слотов завершена на {target_date}")