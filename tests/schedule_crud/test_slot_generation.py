from datetime import date, time
from src.domain.slot_generator import DomainSlotGenerator


def test_slot_generation_basic():
    room_id = "00000000-0000-0000-0000-000000000000"
    target_date = date(2026, 6, 15)

    slots = DomainSlotGenerator.generate_intervals(
        room_id=room_id,
        target_date=target_date,
        start_time=time(9, 0),
        end_time=time(10, 0),
    )

    assert len(slots) == 2

    assert slots[0].start_at.hour == 9
    assert slots[0].start_at.minute == 0

    assert slots[1].start_at.hour == 9
    assert slots[1].start_at.minute == 30