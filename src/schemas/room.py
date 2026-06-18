from pydantic import BaseModel
from uuid import UUID


class RoomCreateSchema(BaseModel):
    name: str
    capacity: int
    description: str | None = None


class RoomResponseSchema(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

