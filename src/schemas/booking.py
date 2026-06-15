
from pydantic import BaseModel
from uuid import UUID

class BookingCreateSchema(BaseModel):
    slot_id: UUID