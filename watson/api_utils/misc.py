from datetime import datetime, timedelta

def floor_hour(t: datetime) -> datetime:
    # https://stackoverflow.com/questions/48937900/round-time-to-nearest-hour-python
    # Rounds to previous hour
    return t.replace(second=0, microsecond=0, minute=0, hour=t.hour)

def ceil_hour(t: datetime) -> datetime:
    # https://stackoverflow.com/questions/48937900/round-time-to-nearest-hour-python
    # Rounds to previous hour
    # what. why
    return (datetime(
        2000, 1, 1,
        hour = t.hour, minute=0, second=0, microsecond=0
        ) + timedelta(hours=1)).time()