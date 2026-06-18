import enum
from datetime import datetime, time
from uuid import UUID, uuid4
from sqlalchemy import String, Integer, Time, DateTime, ForeignKey, Enum, Index, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class BookingStatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.USER)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    bookings: Mapped[list["Booking"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Room(Base):
    __tablename__ = "rooms"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    capacity: Mapped[int] = mapped_column(Integer)

    schedules = relationship(
        "Schedule",
        back_populates="room",
        cascade="all, delete-orphan"
    )

    slots = relationship(
        "Slot",
        back_populates="room",
        cascade="all, delete-orphan"
    )

class Schedule(Base):
    __tablename__ = "schedules"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    room_id: Mapped[UUID] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    day_of_week: Mapped[int] = mapped_column(Integer)  # 0 = Понедельник, 6 = Воскресенье
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)

    room = relationship(
        "Room",
        back_populates="schedules"
    )

    __table_args__ = (
        # ТЗ: "После создания расписание изменить нельзя". 
        # Уникальность гарантирует, что на один день недели у комнаты только одно правило.
        UniqueConstraint("room_id", "day_of_week", name="uq_room_day_schedule"),
    )

class Slot(Base):
    __tablename__ = "slots"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    room_id: Mapped[UUID] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    start_at: Mapped[datetime] = mapped_column(DateTime)  # Время начала в UTC
    end_at: Mapped[datetime] = mapped_column(DateTime)    # Время окончания в UTC

    bookings = relationship("Booking",back_populates="slot")
    room = relationship(
        "Room",
        back_populates="slots"
    )

    __table_args__ = (
        # БИЗНЕС-ЗАЩИТА: База намертво заблокирует создание двух одинаковых слотов на одно время
        UniqueConstraint("room_id", "start_at", name="uq_room_slot_start_time"),
    )

class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    # unique=True гарантирует бизнес-правило: один слот — максимум одна запись брони
    slot_id: Mapped[UUID] = mapped_column(ForeignKey("slots.id", ondelete="CASCADE"))
    status: Mapped[BookingStatusEnum] = mapped_column(Enum(BookingStatusEnum), default=BookingStatusEnum.ACTIVE)
    
    slot = relationship("Slot", back_populates="bookings")
    user: Mapped["User"] = relationship(back_populates="bookings")
    __table_args__ = (
        Index(
            "uq_active_booking_per_slot",
            "slot_id",
            unique=True,
            postgresql_where=(status == BookingStatusEnum.ACTIVE)
        ),
    )   


# Высоконагруженный индекс для мгновенного поиска свободных слотов (выполняем лимит 200мс)
Index("ix_slots_room_date", Slot.room_id, Slot.start_at)