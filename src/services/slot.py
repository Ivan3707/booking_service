from uuid import UUID
from datetime import date




class SlotService:

    async def get_available_slots(
        self,
        uow,
        room_id: UUID,
        target_date: date
    ):
        return await uow.slots.get_available_slots(
            room_id=room_id,
            target_date=target_date
        )