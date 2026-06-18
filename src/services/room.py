


class RoomService:

    async def create_room(self, uow, schema):
        async with uow:
            room = await uow.rooms.create(name=schema.name,capacity=schema.capacity,description=schema.description)
            return room

    async def get_rooms(self, uow):
        async with uow:
            return await uow.rooms.get_all()

    async def get_room(self, uow, room_id):
        async with uow:
            return await uow.rooms.get_by_id(room_id)
        