import datetime

def print_error(error_msg):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[ERROR - {current_time}] {error_msg}")