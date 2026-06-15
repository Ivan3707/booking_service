from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from src.repositories.unitofwork import UnitOfWork

async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    """
    Зависимость (Dependency), которая создает чистый UnitOfWork
    для каждого HTTP-запроса и гарантирует его закрытие после ответа.
    """
    uow = UnitOfWork()
    try:
        yield uow
    finally:
        # Даже если в роутере или сервисе бахнет ошибка,
        # этот блок выполнится гарантированно, и база не «потечет»
        await uow.session.close()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UUID:
    """
    Достает JWT-токен из заголовка, проверяет его подпись и срок действия.
    Возвращает UUID пользователя. Если токен битый — сразу кидает 401.
    """
    try:
        # Здесь в реальной жизни будет: payload = jwt.decode(token, SECRET_KEY, ...)
        # user_id = payload.get("sub")
        
        # Для примера представим, что мы успешно распарсили токен:
        user_id = UUID("истинный-uuid-юзера-из-токена") 
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен или срок действия истек",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_admin(user_id: UUID = Depends(get_current_user)) -> UUID:
    """
    Зависимость для админских эндпоинтов. 
    Сначала требует валидный токен (через Depends(get_current_user)), 
    а потом проверяет роль пользователя в базе.
    """
    # Здесь можно сделать запрос к uow.users.get_by_id(user_id) и проверить role == "admin"
    is_admin = True # Временная заглушка для логики
    
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас недостаточно прав для выполнения этого действия"
        )
        
    return user_id