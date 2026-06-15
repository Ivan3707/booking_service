from src.models.models import Room
from src.repositories.base import AbstractRepository

class RoomRepository(AbstractRepository[Room]):
    """Репозиторий для работы с комнатами (переговорками)."""
    model = Room