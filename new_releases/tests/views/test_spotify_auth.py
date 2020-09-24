from mock import patch

from rest_framework import status
from rest_framework.exceptions import APIException
from django.test import TestCase, Client

from new_releases.exceptions import SpotifyTokenRequestInvalidException


class TestAuthAPIView(TestCase):
    def __init__(self, t):
        super(TestAuthAPIView, self).__init__(t)
        self.client = Client()

    def test_get_redirect(self):
        res = self.client.get('/auth')
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)


RAW_TOKEN_SPOTIFY_RESPONSE = {
    'access_token': 'access_token',
    'refresh_token': 'refresh_token',
    'expires_in': 3600,
    'scope': 'scope'
}


class TestAuthCallbackAPIView(TestCase):
    def __init__(self, t):
        super(TestAuthCallbackAPIView, self).__init__(t)

    @patch(
        'new_releases.services.spotify.SpotifyAuthAPIService.get_user_token',
        return_value=RAW_TOKEN_SPOTIFY_RESPONSE
    )
    def test_get_spotify_token(self, mock):
        res = self.client.get('/auth/callback?code=a_test_code')
        mock.assert_called_with('a_test_code')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    @patch(
        'new_releases.services.spotify.SpotifyAuthAPIService.get_user_token',
    )
    def test_spotify_error(self, mock):
        mock.side_effect = SpotifyTokenRequestInvalidException(400)

        res = self.client.get('/auth/callback?code=a_test_code')
        mock.assert_called_with('a_test_code')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(
        'new_releases.services.spotify.SpotifyAuthAPIService.get_user_token',
        return_value=RAW_TOKEN_SPOTIFY_RESPONSE
    )
    def test_fill_session(self, mock):
        res = self.client.get('/auth/callback?code=a_test_code')
        mock.assert_called_with('a_test_code')
        self.assertTrue(self.client.session.get('user_uuid'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    @patch(
        'new_releases.services.spotify.SpotifyAuthAPIService.get_user_token',
    )
    def test_unexpected_error(self, mock):
        mock.side_effect = APIException()
        res = self.client.get('/auth/callback?code=a_test_code')
        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
