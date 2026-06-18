class BusinessException(Exception):
    """Базовое исключение для нашей бизнес-логики"""
    pass

class InvalidScheduleTimeException(BusinessException):
    def __init__(self, message="Время начала раесписания н может быть позже или равно времени окончания"):
        self.message = message
        super().__init__(self.message)
class SlotAlreadyBookedException(BusinessException):
    def __init__(self, message="Этот временной слот уже забронирован"):
        self.message = message
        super().__init__(self.message)

class BookingNotFoundException(BusinessException):
    def __init__(self, message="Бронирование не найдено"):
        self.message = message
        super().__init__(self.message)

class PermissionDeniedException(BusinessException):
    def __init__(self, message="У вас нет прав для изменения этого бронирования"):
        self.message = message
        super().__init__(self.message)

class BadRequestException(BusinessException):
    def __init__(self, message="Некорректный запрос"):
        self.message = message
        super().__init__(self.message)

class SlotNotFoundException(BusinessException):
    def __init__(self, message="Слот не найден"):
        self.message = message
        super().__init__(self.message)

class ScheduleAlreadyExistsException(Exception):
    def __init__(self, message="Расписание Уже существует"):
        self.message = message
        super().__init__(self.message)


class BookingAlreadyExistsException(Exception):
    pass


class NotFoundException(Exception):
    pass
