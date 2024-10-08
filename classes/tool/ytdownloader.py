from pytube import YouTube,Playlist
from ._base import Tool

class YTDownloader(Tool):
    def Download(self,URL) -> None:
        try:
            Download_Instance = Playlist(URL)
            for Video in Download_Instance.videos:
                try: Video.streams.filter(file_extension='mp4').order_by('resolution').desc().first().download()
                except Exception as e: continue

        except KeyError: 
                Download_Instance = YouTube(URL)
                Download_Instance.streams.filter(file_extension='mp4').order_by('resolution').desc().first().download()