import json

from googleapiclient.discovery import build


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Channel для ютуб-канала"""

    api_key: str = 'AIzaSyDW53bmm5mfkQ_HFjjLpyHUtE0GTKuUXeo '  # os.getenv('YT_API_KEY')
    youtube: any

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        printj(channel)
