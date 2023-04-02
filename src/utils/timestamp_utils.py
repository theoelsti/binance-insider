import datetime

def format_timestamp(timestamp):
    # Convert the timestamp to a timedelta object
    time_difference = datetime.timedelta(seconds=timestamp)

    # Extract the days, hours, and minutes from the timedelta object
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes = remainder // 60
    
    # Format the time difference
    formatted_time = []
    if days > 0:
        formatted_time.append(f"{days} day{'s' if days > 1 else ''}")

    if hours > 0:
        formatted_time.append(f"{hours} hour{'s' if hours > 1 else ''}")

    if minutes > 0:
        formatted_time.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    return ', '.join(formatted_time)

