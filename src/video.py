import os

from Tools.scripts import google
from google.auth.exceptions import DefaultCredentialsError
from googleapiclient.discovery import build


class Video:

    def __init__(self, video_id: str):
        self.video_id = video_id
        try:
            self.api_key = os.getenv('API_KEY')

            self.youtube = build('youtube', 'v3', developerKey=self.api_key)

            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video_id
                                                        ).execute()
            self.title: str = video_response['items'][0]['snippet']['title']
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
        except Exception:
            print("Введён неверный id")
            self.title = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id


