import os

        
# For Windows
def schedule_file_deletion(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    # s.enter(60, 1, lambda: os.remove(file_path) if os.path.exists(file_path) else None, ())
    