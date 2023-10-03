import datetime
import json
import os

import isodate
from googleapiclient.discovery import build


class PlayList:

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.api_key = os.getenv('API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        self.playlist_name = self.youtube.playlists().list(id=playlist_id, part='snippet,contentDetails',
                                                           maxResults=50).execute()
        "https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"
        self.title = self.playlist_name["items"][0]["snippet"]["title"]
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id

        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

        self.video_response = self.youtube.videos().list(part='contentDetails,statistics,snippet',
                                                         id=','.join(self.video_ids)
                                                         ).execute()

    @property
    def total_duration(self):
        """возвращает объект класса `datetime.timedelta`
        с суммарной длительность плейлиста"""

        timedelta_object = datetime.timedelta()

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            h = str(duration)[:1]
            m = str(duration)[2:4]
            s = str(duration)[5:]
            timedelta_object += datetime.timedelta(seconds=int(s), minutes=int(m), hours=int(h))
        return timedelta_object

    def show_best_video(self):

        top_video_like = self.video_response["items"][0]

        for video in self.video_response["items"]:
            if video["statistics"]["likeCount"] > top_video_like["statistics"]["likeCount"]:
                top_video_like = video
        return "https://youtu.be/" + top_video_like["id"]

