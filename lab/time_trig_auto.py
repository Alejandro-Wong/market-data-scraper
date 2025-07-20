import time 
import datetime
from datetime import datetime, timedelta, time


market_open = datetime.now().replace(hour=9, minute=30, microsecond=0)
market_close = datetime.now().replace(hour=16, minute=0, microsecond=0)


def time_until(time: time) -> str:
    curr_dt = datetime.now().replace(microsecond=0)
    return time - curr_dt




