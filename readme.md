# Media Converter Tool For CS50 Final Project By Femi Kuye

#### Author Name: Femi Kuye

#### Year: 2023

#### City: Ibadan

#### Country: Nigeria

#### Presentation Video Link: https://youtu.be/wQfp3rOqFWs

## Descriptions

This media converter software is helpful for a quick media conversion from one format to another.
Imagine you need to upload a media file to a website but you do not have the format required, this is the problem I seek to solve by creating this web based software that help to convert your media files to different formats.

## Functionalities

1. Image Converter
   This feature allow users to convert images from one format to another format. E.g. From JPEG to PNG
2. Audio Converter
   Just like the image converter, this feature allows users to convert audios from one format to another format
3. Video Converter
   This feature allow users to convert their videos from one format to another. Though this feature is extremly slow because of the time it takes to proccess each single frame in videos, if you have a powerful computer it will make a different.

## Make Up Of This Software

### Front End

**External Assets:** Bootstrap, JQuery, FontAwesome
**Custom Assets:**
**style.css** : This file contain all my custom styles for the UI to look better. This is an addition to what the bootstrap CSS offered. This file is inside the /static/css/ directory
**script.js** : This file contain the Ajax code the i write to submit forms to the server. It is located in the /static/js/ Directory

**HTML Pages**
**index.html** : This is the file that describe the home page. It shows the link to all the features on the website
**audio-converter.html** : This file provide the interface for converting audio files
**image-converter.html** : This is for the image conversion interface/form
**video-converter.html** : This file contain the interface for converting videos to different formats

#### Front End Sumary

What the front end provide is simply the interface for users to upload and send their media files to the server so the server can convert it to the selected format. All users has to do is just to Load the page, click the upload icon to select the media files from their computers, Select the format they want the media file to be converted to and finally hit the convert button.
The last action will send the form to the server for processing and then return the link to download the converted file. If Users upload multiple files, they have the option to download converted files individually or download all together in a zip file.

### Back End

**Packages/Libraries Used**

1. Flask: Flask is used for the webserver
2. ffmpeg: Ffmpeg is used for the videos and audio convertion. Without it, the application can not work
3. ffmpeg-python: This library is used as a python wrapper for ffmpeg which makes working with ffmpeg easy
4. Pillow: This is used for the images conversion specifically
5. apscheduler: After user has converted media files, the media stay on the server, in other to prevent this file to be on the server for a long time, we have to schedule the time it should be deleted. Ofcourse we must give some time for the user to download the converted files before deleting it. This is why am using apscheduler sche class to schedule the time for the files to be deleted after convertion.

**Modules**
Here is the list of modules i have created for each features and functionalities of this project. The modules files are inside the /modules/ directory

1. **AudioConverter.py**: This file is used to write the audio convertion aspect of the project. Inside of this file i import different packages that is needed for this purpose then i create a variable called "audio_formats", this is used to store all the audio formats that is supported by this software. This variable is later passed to the front end which i use to display available audio formats to the users. It is also passed to the script.js which allow me to write a check on every file the user attempt to upload if the format is supported or not. Only supported formats is allowed to be uploaded.

Next in this file is the **Converter** class which contain two functions, the **init** function which is used to get the arguments passed to the class during instantiation. These parameters are **upload_path and scheduler** upload_path is holding the path to the file to be converted while scheduler will hold the instatition of the **BackgroundScheduler** class that is used to schedule when both the uploaded file and the converted file will be deleted.

The second function inside of the **Converter** class is the **convert_audio** function which takes the **file_obj and output_format** as arguments. This function perform the conversion by calling another module, the **FfmpegWarapper.py** file.

2. **VideoConverter.py**: This file is used to handle video conversion. It follows the same concept as **AudioConverter.py**

3. **ImageConverter.py**: The code in this file follow the same concept as **VideoConverter.py and AudioConverter.py** The difference is first, it handle Image conversion, second, it uses the PILLOW library to do the image conversion. instead of ffmpeg.

4. **FfmpegWrapper.py**: This file uses the **ffmpeg-python** package to convert video and audio files. This file is used by both **VideoConverter.py and AudioConverter.py**

5. **TaskScheduler.py**: This module is called by the task scheduler to delete files

6. **FilesCompressor**: In case users convert multiple files and wanting to download them at once, we need a way to compress all the files into one zip file for the users to download. This is where this file is usefull.
