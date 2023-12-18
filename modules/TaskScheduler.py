import schedule
import sched
import time
import os
s = sched.scheduler(time.time, time.sleep)
# def schedule_file_deletion(file_path):
#     # Schedule file deletion after one hour
#     schedule.every().hour.do(lambda: os.remove(file_path) if os.path.exists(file_path) else None)

#     # Run the schedule in the background
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# def schedule_file_deletion(file_paths):
#     for file_path in file_paths:
#         schedule.every().hour.do(lambda: os.remove(file_path) if os.path.exists(file_path) else None)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)\
        
# For Windows
def schedule_file_deletion(file_path):
    s.enter(3600, 1, lambda: os.remove(file_path) if os.path.exists(file_path) else None, ())