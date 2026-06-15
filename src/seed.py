import asyncio
from datetime import time
from src.repositories.unitofwork import UnitOfWork
from src.models.models import User, RoleEnum, Room, Schedule


async def seed_data():
    print("Запуск наполнения базы данных тестовыми данными...")
    uow = UnitOfWork()

    async with uow:
        # --- 1. ПРОВЕРКА НА ПУСТОТУ ---
        # Чтобы не дублировать данные при повторном запуске, проверим, есть ли уже пользователи
        # Для этого временно сделаем прямой запрос через сессию UOW
        from sqlalchemy import select
        existing_users = await uow.session.execute(select(User))
        if existing_users.scalars().first():
            print("База данных уже содержит данные. Наполнение пропущено.")
            return

        print("Создание пользователей...")
        admin = User(email="admin@company.com", role=RoleEnum.ADMIN)
        user1 = User(email="employee1@company.com", role=RoleEnum.USER)
        user2 = User(email="employee2@company.com", role=RoleEnum.USER)
        
        uow.session.add_all([admin, user1, user2])

        print("Создание переговорок...")
        big_room = Room(name="Большая переговорка", capacity=20, description="Маркерная доска, проектор, флипчарт")
        small_room = Room(name="Малая стекляшка", capacity=4, description="Уютная комната для созвонов")
        
        uow.session.add_all([big_room, small_room])
        # Делаем flush, чтобы у комнат сгенерировались UUID, которые понадобятся для расписания
        await uow.session.flush()

        print("Создание расписания для переговорок...")
        schedules = []

        # Расписание для Большой переговорки: Понедельник(0) - Пятница(4) с 09:00 до 18:00
        for day in range(5):
            sch = Schedule(
                room_id=big_room.id,
                day_of_week=day,
                start_time=time(9, 0),
                end_time=time(18, 0)
            )
            schedules.append(sch)

        # Расписание для Малой стекляшки: Суббота(5) и Воскресенье(6) круглосуточно (почти)
        for day in [5, 6]:
            sch = Schedule(
                room_id=small_room.id,
                day_of_week=day,
                start_time=time(0, 0),
                end_time=time(23, 59)
            )
            schedules.append(sch)

        uow.session.add_all(schedules)
        
        # В конце блока async with произойдет автоматический commit()
        print("База данных успешно наполнена тестовыми данными!")


if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(seed_data())