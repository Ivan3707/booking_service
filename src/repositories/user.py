from src.models.models import User
from src.repositories.base import AbstractRepository


class UsersRepository(AbstractRepository[User]):
    """Репозиторий для работы с пользователями."""
    model = User