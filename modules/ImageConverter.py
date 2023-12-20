import os
from modules import error_response , ROOT_URL 
from modules.TaskScheduler import schedule_file_deletion
import io
from pathlib import Path
import uuid
from PIL import Image
import datetime

image_formats = [
    'jpeg', 'jpg', 'png', 'tiff', 'bmp', 'gif', 'eps', 'ai', 'raw', 'heic'
]

class Converter:
    def __init__(self, upload_path, scheduler):
        self.error_message = ""
        self.upload_path = f"{upload_path}/images"
        self.error = ""
        if not os.path.exists(self.upload_path):
            os.makedirs(self.upload_path, exist_ok=True)
        self.scheduler = scheduler
    def convert_image(self, file_obj, output_format):
        uploaded_file = os.path.join(self.upload_path, file_obj.filename)
        if os.path.exists(uploaded_file):
            uploaded_file = os.path.join(self.upload_path,str(uuid.uuid4()) + file_obj.filename)
        
        file_obj.save(uploaded_file)
        output_name =  f"{Path(file_obj.filename).stem}.{output_format}"
        output_file = os.path.join(self.upload_path, output_name)

        if os.path.exists(output_file):
            output_name =  f"{str(uuid.uuid4()) + Path(file_obj.filename).stem}.{output_format}"
            output_file = os.path.join(self.upload_path, output_name)
        
        self.scheduler.add_job(schedule_file_deletion, 'date', run_date=datetime.datetime.now() + datetime.timedelta(minutes=60), args=[uploaded_file])
       
        # Define the input and output streams
        do_convert = self.do_convert_image(uploaded_file, output_file, output_format)

        if do_convert:
            self.scheduler.add_job(schedule_file_deletion, 'date', run_date=datetime.datetime.now() + datetime.timedelta(minutes=60), args=[output_file])
            return {
                "file_url": f"{ROOT_URL}/download/image/{output_name}"
            }
        else:
            return error_response(self.error)
    

    def do_convert_image(self, input_path, output_path, output_format):
        try:
            img = Image.open(input_path)
            img.save(output_path, format=output_format)
            return True
        except Exception as e:
            self.error = f"Error during image conversion: {e}"
            return False
        