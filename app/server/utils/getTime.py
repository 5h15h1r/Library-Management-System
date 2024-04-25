from datetime import datetime
import time


def timeInSeconds(current_date):
    end_of_day = datetime(
        current_date.year, current_date.month, current_date.day, 23, 59, 59
    )
    # Calculate local offset time
    local_timezone_offset_seconds = time.timezone
    remaining_time = end_of_day - current_date
    expiration_time = remaining_time.seconds - +(-local_timezone_offset_seconds)
    return expiration_time
