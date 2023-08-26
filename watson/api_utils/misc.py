from datetime import datetime, timedelta

def floor_hour(t: datetime) -> datetime:
    # https://stackoverflow.com/questions/48937900/round-time-to-nearest-hour-python
    # Rounds to previous hour
    return t.replace(second=0, microsecond=0, minute=0, hour=t.hour)

def ceil_hour(t: datetime) -> datetime:
    # https://stackoverflow.com/questions/48937900/round-time-to-nearest-hour-python
    # Rounds to previous hour
    return t.replace(second=0, microsecond=0, minute=0, hour=t.hour) + timedelta(hours=1)