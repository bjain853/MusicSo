from abc import ABC, abstractmethod


class Streaming_Provider(ABC):
    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def get_access_token(self):
        pass

    @abstractmethod
    def refresh_access_token(self, refresh_token: str):
        pass

    @abstractmethod
    def create_playlist(self):
        pass

    @abstractmethod
    def get_playlist(self):
        pass
