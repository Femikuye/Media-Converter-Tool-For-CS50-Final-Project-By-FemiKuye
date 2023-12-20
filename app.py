import os
from flask import Flask , request , render_template, send_file
from modules import error_response , APP_PORT , ROOT_URL
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_FOLDERS = "tmp_files"
TMP_PATH = f"{ROOT_DIR}/{TMP_FOLDERS}"
scheduler = BackgroundScheduler()
scheduler.start()

@app.route("/")
def index():
    return render_template("index.html", navActive='home')

@app.route("/convert-audios")
def convert_audios():
    from modules.AudioConverter import audio_formats
    return render_template("audio-converter.html", audioFormats=audio_formats, navActive='audio')

@app.route("/convert-videos")
def convert_videos():
    from modules.VideoConverter import video_formats
    return render_template("video-converter.html", videoFormats=video_formats, navActive='video')

@app.route("/convert-images")
def convert_images():
    from modules.ImageConverter import image_formats
    return render_template("image-converter.html", imageFormats=image_formats, navActive='image')

@app.route("/media-converter", methods=["POST"])
def media_converter():
    converter = request.form.get("converter")
    if not converter:
        return error_response("Invalid Request")
    if "file" not in request.files:
        return error_response("No file to process")
    file  = request.files["file"]
    if file.filename == "":
        return error_response("No file to process")
    
    output_format  = request.form.get("convertTo")
    input_format = request.form.get("file-format")
    if converter == "audio-converter":
        from modules.AudioConverter import Converter
        myAudioConverter = Converter(TMP_PATH, scheduler)
        return myAudioConverter.convert_audio(file, output_format)
    elif converter == "video-converter":
        from modules.VideoConverter import Converter
        myVideoConverter = Converter(TMP_PATH, scheduler)
        return myVideoConverter.convert_video(file, output_format)
    elif converter == "image-converter":
        from modules.ImageConverter import Converter
        myImageConverter = Converter(TMP_PATH, scheduler)
        return myImageConverter.convert_image(file, output_format)
    

@app.route("/download/<file_type>/<file_path>")
def download(file_type, file_path):
    if file_type == "audio":
         file_path = f"{TMP_PATH}/audios/{file_path}"
         if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
    elif file_type == "zip":
         file_path = f"{TMP_PATH}/{file_path}"
         if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
    elif file_type == "video":
         file_path = f"{TMP_PATH}/videos/{file_path}"
         if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
    elif file_type == "image":
         file_path = f"{TMP_PATH}/images/{file_path}"
         if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
         
    return "<h3>Error! File not found</h3>"

@app.route("/bulk-files-download", methods=["POST"])
def bulk_files_download():
    converter = request.form.get("converter")
    if not converter:
        return error_response("Invalid Request")
    files_links = request.form.getlist("files_links[]")
    if not files_links:
        return error_response("No file to download")
    files_dir = ""
    if converter == "audio-converter":
        files_dir = f"{TMP_PATH}/audios"
    elif converter == "video-converter":
        files_dir = f"{TMP_PATH}/videos"
    elif converter == "image-converter":
        files_dir = f"{TMP_PATH}/images"
    files_list = []
    for link in files_links:
        if os.path.exists(f"{files_dir}/{link}"):
            files_list.append(
                {"name": link, "dir": f"{files_dir}/{link}"}
            )
    if len(files_list) < 1:
        return error_response("No files to download")
    import uuid
    zip_name = f"{str(uuid.uuid4())}.zip"
    zip_output_path = f"{TMP_PATH}/{zip_name}"
    from modules.FilesCompressor import zipper
    compressor = zipper(files_list, zip_output_path, files_dir)
    if compressor.create_podcast_zip() and os.path.exists(zip_output_path):
        import datetime
        from modules.TaskScheduler import schedule_file_deletion
        scheduler.add_job(schedule_file_deletion, 'date', run_date=datetime.datetime.now() + datetime.timedelta(minutes=60), args=[zip_output_path])
        return {
            "download_url": f"{ROOT_URL}/download/zip/{zip_name}"
        }
    else:
        return error_response("Fail to create downloadable zip")
    
if __name__ == '__main__':
    app.run(debug=True, port=APP_PORT)