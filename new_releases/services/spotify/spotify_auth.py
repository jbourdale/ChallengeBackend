from django.conf import settings

from datetime import datetime, timedelta
import base64, json, requests
from concurrent.futures import as_completed

from new_releases.exceptions import SpotifyTokenRequestInvalidException
from new_releases.models.spotify.token import SpotifyToken


class SpotifyAuthAPIService():
    AUTH_URL = "https://accounts.spotify.com/authorize/"
    TOKEN_URL = "https://accounts.spotify.com/api/token/"
    CALLBACK_URL = settings.SPOTIFY_CALLBACK_URL
    RESPONSE_TYPE = "code"
    HEADER = "application/x-www-form-urlencoded"
    SCOPE = settings.SPOTIFY_AUTH_SCOPE
    CLIENT_ID = settings.SPOTIFY_CLIENT_ID
    CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET

    def __init__(self):
        self.token = None

    def get_user(self):
        return self._get_auth(
            self.CLIENT_ID, f"{self.CALLBACK_URL}/callback", self.SCOPE,
        )

    def get_user_token(self, code):
        return self._get_token(
            code, self.CLIENT_ID, self.CLIENT_SECRET, f"{self.CALLBACK_URL}/callback"
        )

    def refresh_auth(self, spotify_user):
        body = {"grant_type": "refresh_token", "refresh_token": spotify_user.refresh_token}

        encoded = base64.b64encode(f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode()).decode()
        post_refresh = requests.post(
            self.TOKEN_URL,
            data=body,
            headers = {
                "Content-Type": self.HEADER,
                "Authorization": f"Basic {encoded}",
            }
        )
        p_back = json.dumps(post_refresh.text)
        return self._handle_token(json.loads(post_refresh.text))

    def _get_auth(self, client_id, redirect_uri, scope):
        return (
            f"{self.AUTH_URL}"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope={scope}"
            "&response_type=code"
        )

    def _get_token(self, code, client_id, client_secret, redirect_uri):
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        encoded = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers = {
            "Content-Type": self.HEADER,
            "Authorization": f"Basic {encoded}",
        }

        post = requests.post(self.TOKEN_URL, params=body, headers=headers)
        return self._handle_token(json.loads(post.text))

    def _handle_token(self, response):
        if "error" in response:
            print(response)
            raise SpotifyTokenRequestInvalidException(f"{response['error']}")
        return response
