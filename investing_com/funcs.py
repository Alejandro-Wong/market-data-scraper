import math

def round_time(dt):
    """
    Round a time to the nearest 5 minutes
    """
    total_minutes = dt.hour * 60 + dt.minute
    rounded_minutes = math.ceil(total_minutes / 5) * 5
    new_hour = rounded_minutes // 60
    new_minute = rounded_minutes % 60

    return dt.replace(hour=new_hour, minute=new_minute, second=0, microsecond=0)




