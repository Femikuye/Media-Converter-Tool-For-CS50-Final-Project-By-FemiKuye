import os
from modules import error_response , ROOT_URL 
from modules.TaskScheduler import schedule_file_deletion
from modules.FfmpegWrapper import convert_audio as audio_converter
import io
from pathlib import Path
import uuid

import datetime

audio_formats = [
    'mp3', 'wav', 'ogg', 'aiff', 'au', 'aac', 'flac', 'wma', 'pcm'
]

class Converter:
    def __init__(self, upload_path, scheduler):
        self.error_message = ""
        self.upload_path = f"{upload_path}/audios"
        if not os.path.exists(self.upload_path):
            os.makedirs(self.upload_path, exist_ok=True)
        self.scheduler = scheduler
    def convert_audio(self, file_obj, output_format):
        uploaded_file = os.path.join(self.upload_path, file_obj.filename)
        if os.path.exists(uploaded_file):
            uploaded_file = os.path.join(self.upload_path,str(uuid.uuid4()) + file_obj.filename)
        
        file_obj.save(uploaded_file)
        output_name =  f"{Path(file_obj.filename).stem}.{output_format}"
        output_file = os.path.join(self.upload_path, output_name)

        if os.path.exists(output_file):
            output_name =  f"{str(uuid.uuid4()) + Path(file_obj.filename).stem}.{output_format}"
            output_file = os.path.join(self.upload_path, output_name)
        
        self.scheduler.add_job(schedule_file_deletion, 'date', run_date=datetime.datetime.now() + datetime.timedelta(minutes=75), args=[uploaded_file])
       
        # Define the input and output streams
        do_convert = audio_converter(uploaded_file, output_file)
        if do_convert["success"]:
            self.scheduler.add_job(schedule_file_deletion, 'date', run_date=datetime.datetime.now() + datetime.timedelta(minutes=75), args=[output_file])
            return {
                "file_url": f"{ROOT_URL}/download/audio/{output_name}"
            }
        else: 
            return error_response(do_convert["msg"])
        