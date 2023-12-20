import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import shutil


class zipper:
    def __init__(self, files_path_list: Path, output_zip_path: Path, files_dir: Path):
        self.files_dir_list = files_path_list
        self.output_zip_path = output_zip_path
        self.files_dir = files_dir
        self.error = ""
    def create_podcast_zip(self):
        try:
            with ZipFile(self.output_zip_path, mode="w", compression=ZIP_DEFLATED) as zfile:
                for file in self.files_dir_list:
                    zfile.write(file["dir"], arcname=file["name"])

        except Error:
            self.error = "An Error Occured"
            return False
            # shutil.rmtree(self.files_dir, onerror=onerror)
            
        return True