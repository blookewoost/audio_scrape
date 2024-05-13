import pytube
import os
from tkinter import filedialog
from Video import Video

class Playlist:
    def __init__(self, _url, _name):
        self.url = _url
        self.name = _name
        self.playlist_object = pytube.Playlist(self.url)
        self.collect_videos()
        self.select_folder()
        self.save_audio()

    def collect_videos(self):
        self.videos = []
        for url in self.playlist_object.video_urls:
            self.videos.append(Video(url))

    def select_folder(self):
        sdir = filedialog.askdirectory()
        self.folder = sdir


    def save_audio(self):

        for video in self.videos:
            filename = video.title + ".mp3"
            filename = self.filename_correction(filename)

            if filename in os.listdir(self.folder):
                print("A copy of {} already exists on disk, skipping it.".format(filename))
            else:
                stream = self.stream_select(video)
                stream.download(output_path=self.folder + '/' + filename)

    '''
    Convert the video title into an acceptable filename for the .mp3
    '''
    def filename_correction(self, filename):
        
        invalid_chars = '<>:"/\\|?*'
        new_filename = []

        for char in filename:
            if char in invalid_chars:
                new_filename.append('_')  # Replace invalid character with underscore
            else:
                new_filename.append(char)

        new_filename = ''.join(new_filename)
        return new_filename
    
    '''
    This method is no longer in use.
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

    def stream_select(self, video):

        streams = video.video_object.streams.filter(only_audio=True)
        quality = []

        # Filter the available audio streams
        for stream in streams:
            quality.append(int(stream.abr.removesuffix('kbps')))

        hq = max(quality)
        idx = quality.index(hq)

        return streams[idx]
            

        
        