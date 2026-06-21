from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID

from src.api.dependencies import get_uow
from src.core.unitofwork import UnitOfWork
from src.services.room import RoomService
from src.schemas.room import RoomCreateSchema, RoomResponseSchema


router = APIRouter()

service = RoomService()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_room(schema: RoomCreateSchema, uow: UnitOfWork = Depends(get_uow)):
    room = await service.create_room(uow, schema)

    return {
        "id": room.id,
        "name": room.name
    }


@router.get("")
async def get_rooms(uow: UnitOfWork = Depends(get_uow)):
    rooms = await service.get_rooms(uow)
    return rooms


@router.get("/{room_id}")
async def get_room(room_id: UUID, uow: UnitOfWork = Depends(get_uow)):
    room = await service.get_room(uow, room_id)

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    return room