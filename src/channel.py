import json
import os
import ast

from googleapiclient.discovery import build


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Channel для ютуб-канала"""

    api_key: str
    youtube: any

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_name = None
        self.api_key = os.getenv('API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.channel_id = channel_id
        self._channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self._load_par()

    def _load_par(self):
        data = json.dumps(self._channel, indent=2, ensure_ascii=False)
        data = json.loads(data)
        self.title = data["items"][0]["snippet"]["title"]
        self.description = data["items"][0]["snippet"]["description"]
        self.url = data["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.subscriberCount = data["items"][-1]["statistics"]["subscriberCount"]
        self.videoCount = data["items"][-1]["statistics"]["videoCount"]
        self.viewCount = data["items"][-1]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        printj(channel)

    def get_service(self):
        return self.youtube

    def to_json(self, file):
        data = {
            "channel_id": self.channel_id,
            "title": self.channel_name,
            "description": self.description,
            "url": self.url,
            "subscriberCount": self.subscriberCount,
            "videoCount": self.videoCount,
            "viewCount": self.viewCount
        }
        with open(file, 'w') as f:
            f.write(json.dumps(data, indent=4))
