import os
from flask import Flask , request , render_template, redirect, url_for, send_file
from modules import error_response , APP_PORT , ROOT_URL
import threading  # Import the threading module for running the schedule in a separate thread
from modules.TaskScheduler import run_schedule


app = Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_FOLDERS = f"{ROOT_DIR}/tmp_files"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download-youtube-videos", methods=["POST", "GET"])
def download_youtube_videos():
    if request.method == "GET":
        return render_template("download-youtube.html")
    elif request.method == "POST":
        if not request.form.get("youtube-video-link"):
            return error_response("Please input a youtube link")
        
        if not request.form.get("user-id"):
            return error_response("Invalid Request")
        
        video_url = request.form.get("youtube-video-link")
        user_id = request.form.get("user-id")
        from modules.YouTube import downloader
        my_downloader = downloader()
        return my_downloader.download_youtube_video(video_url, user_id)
    
    return render_template("download-youtube.html")

@app.route("/convert-audios")
def convert_audios():
    from modules.AudioConverter import audio_formats
    return render_template("audio-converter.html", audioFormats=audio_formats)

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
        myAudioConverter = Converter(TMP_FOLDERS)
        return myAudioConverter.convert_audio(file, output_format)
    

@app.route("/download/<file_type>/<file_path>")
def download(file_type, file_path):
    if file_type == "audio":
         return send_file(f"{TMP_FOLDERS}/audios/{file_path}", as_attachment=True)
    
if __name__ == '__main__':
    # schedule_thread = threading.Thread(target=run_schedule)
    # schedule_thread.start()
    app.run(debug=True, port=APP_PORT)