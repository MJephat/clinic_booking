from datetime import datetime, timedelta, time


SLOT_DURATION = 30  # minutes


def generate_time_slots(start: time, end: time) -> list[time]:
    """
    Generate 30-minute appointment slots between start and end time.
    Example:
    09:00-11:00 -> 09:00, 09:30, 10:00, 10:30
    """

    slots = []

    current = datetime.combine(datetime.today(), start)
    finish = datetime.combine(datetime.today(), end)

    while current < finish:
        slots.append(current.time())
        current += timedelta(minutes=SLOT_DURATION)

    return slots


def combine_date_and_time(date_value, time_value):
    return datetime.combine(date_value, time_value)


def is_past_slot(slot: datetime):
    return slot < datetime.now()