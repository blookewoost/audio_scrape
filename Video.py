import pytube
from pytube import YouTube

class Video:
    def __init__(self, _url):
        self.url = _url
        try:
            self.video_object = pytube.YouTube(self.url)
            print(self.video_object.title)
        except Exception as E:
            print("Creating video object failed for url: {}, the following exception was thrown {}".format(self.url, E))

        self.get_video_details()

    def get_video_details(self):
        self.title = self.video_object.title

    
