import urllib.parse
import requests
import os
import Streaming_Provider


class Spotify(Streaming_Provider):
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        self.auth_uri = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base_url = "https://api.spotify.com/v1/"

    def authenticate(self):
        scope = "user-read-email user-read-private playlist-read-private playlist-modify-private playlist-modify-public"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": scope,
            "redirect_uri": self.redirect_uri,
            "show_dialog": True,
            "response_type": "code",
        }
        auth_url = f"{self.auth_uri}?{urllib.parse.urlencode(params)}"
        return auth_url

    def get_access_token(self, code):
        req_body = {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(self.token_url, data=req_body)
        return response.json()

    def get_playlist(self, auth_token, playlist_id):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(
            f"{self.api_base_url}/playlists/{playlist_id}", headers=headers
        )
        return response.json()

    def refresh_access_token(self, refresh_token):
        req_body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(self.token_url, data=req_body)
        return response.json()

    def create_playlist(self, user_id):
        req_body = {
            "name": "MusicSo Share",
            "description": "Add new songs to this playlist to share with your friends on MusicSo",
            "public": True,
        }
        response = requests.post(
            f"{self.api_base_url}/users/{user_id}/playlists", data=req_body
        )
        return response.json()  # store id for user
