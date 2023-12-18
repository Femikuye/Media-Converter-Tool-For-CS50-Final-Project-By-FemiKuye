from pytube import YouTube

# Pytube Documentation At https://pytube.io/en/latest/user/quickstart.html#downloading-a-video
downloads_list = {}
class downloader:
    # def __init__(self) -> None:
    #     self.me = "Me"
    def download_youtube_video(self, link, user_id):
        import validators
        if not validators.url(link):
            return {"msg": "Invalid Url"}, 400
        try:
            yt_object = YouTube(
                link,
                on_progress_callback= self.download_progress_callback,
                on_complete_callback= self.download_complete_callback,
                # proxies=my_proxies,
                # use_oauth=False,
                # allow_oauth_cache=True
            )
            video_title = yt_object.title
            video_thumbnail = yt_object.thumbnail_url
            downloads_list[user_id] = {
                "title": yt_object.title,
                "thumbnail": video_thumbnail
            }
            # streams.get_highest_resolution()
            streams = yt_object.streams.get_highest_resolution() #filter(progressive=True)
            streams.download()
            return {"title": video_title, "thumbnail": video_thumbnail}
        except VideoUnavailable:
            return {"msg": "Video is unavaialable"}
        
    def download_progress_callback(self, stream, shunk, size):
        print(f"File zile {size}")
        return

    def download_complete_callback(self, stream, file_path):
        print(f"Download completed. File path is {file_path}")
        return