import pytube
import pafy
import os
from Video import Video

class Playlist:
    def __init__(self, _url, _name):
        self.url = _url
        self.name = _name
        self.playlist_object = pytube.Playlist(self.url)
        self.collect_videos()
        self.create_folder()
        self.save_audio()

    def collect_videos(self):
        self.videos = []
        for url in self.playlist_object.video_urls:
            self.videos.append(Video(url))
            
    def create_folder(self):
        self.folder = './' + self.name
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        else:
            print("The folder for this playlist already exists.")

    def save_audio(self):
        for video in self.videos:
            filename = video.title + ".mp3"
            if filename in os.listdir(self.folder):
                print("A copy of {} already exists on disk, skipping it.".format(filename))
            else:
                stream = self.get_audio(video)
                stream.download(output_path=self.folder + '/' + filename)
    
    '''
    FIXME dynamically select the highest quality audio stream. Currently we assume a 160kbps stream exists.
    '''
    def get_audio(self, video):

        # Filter the available audio streams
        for stream in video.video_object.streams.filter(only_audio=True):
            if stream.abr == "160kbps":
                itag = stream.itag
            else:
                print("Ignoring stream with low abr: {}".format(stream.abr))

        if itag:
            s = video.video_object.streams.get_by_itag(itag)
            return s
        else:
            raise Exception("No high quality audio streams were found for video: {}".format(video.video_object.title))

        
        