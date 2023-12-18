import os
from modules import error_response , ROOT_URL 
from modules.TaskScheduler import schedule_file_deletion
from modules.FfmpegWrapper import convert_audio as audio_converter
import io
from pathlib import Path
import uuid
import threading  # Import the threading module for running the schedule in a separate thread



audio_formats = [
    'mp3', 'wav', 'ogg'
]

class Converter:
    def __init__(self, upload_path):
        self.error_message = ""
        self.upload_path = f"{upload_path}/audios"
    def convert_audio(self, file_obj, output_format):
        uploaded_file = os.path.join(self.upload_path, file_obj.filename)
        if os.path.exists(uploaded_file):
            uploaded_file = os.path.join(self.upload_path,str(uuid.uuid4()) + file_obj.filename)
        
        output_name =  f"{Path(file_obj.filename).stem}.{output_format}"
        output_file = os.path.join(self.upload_path, output_name)

        if os.path.exists(output_file):
            output_name =  f"{str(uuid.uuid4()) + Path(file_obj.filename).stem}.{output_format}"
            output_file = os.path.join(self.upload_path, output_name)
        
        file_obj.save(uploaded_file)
        # schedule_file_deletion(uploaded_file)
        deletion_thread = threading.Thread(target=schedule_file_deletion, args=([uploaded_file, output_file]))
        deletion_thread.start()
        # Define the input and output streams
        do_convert = audio_converter(uploaded_file, output_file)
        if do_convert.success:
            return {
                "file_url": f"{ROOT_URL}/download/audio/{output_name}"
            }
        else: 
            return error_response(do_convert.msg)
        