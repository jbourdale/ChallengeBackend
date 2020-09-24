from mock import patch

from rest_framework import status
from django.utils import timezone
from django.test import TestCase

from new_releases.models import SpotifyUserModel, ArtistsRefreshModel


class TestArtistReleasesAPIView(TestCase):
    def __init__(self, t):
        super(TestArtistReleasesAPIView, self).__init__(t)

    def test_cookie_provided(self):
        res = self.client.get('/api/artists')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch(
        'new_releases.models.SpotifyUserModel.objects.get',
        return_value=None
    )
    def test_cookie_unvalid(self, mock):
        session = self.client.session
        session['user_uuid'] = 'uuid'
        session.save()
        res = self.client.get('/api/artists')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    @patch(
        'new_releases.views.artists.ArtistReleasesAPIView._refresh_artists',
    )
    @patch(
        'new_releases.models.SpotifyUserModel.objects.get',
        return_value=SpotifyUserModel()
    )
    @patch(
        'new_releases.views.artists.ArtistReleasesAPIView._get_latest_refresh',
        return_value=ArtistsRefreshModel(date_refresh=timezone.now())
    )
    def test_get_from_db(self, artists_mock, spotify_mock, refresh_mock):
        session = self.client.session
        session['user_uuid'] = 'uuid'
        session.save()

        res = self.client.get('/api/artists')
        refresh_mock.assert_not_called()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    @patch(
        'new_releases.views.artists.ArtistReleasesAPIView._refresh_artists',
    )
    @patch(
        'new_releases.models.SpotifyUserModel.objects.get',
        return_value=SpotifyUserModel()
    )
    @patch(
        'new_releases.views.artists.ArtistReleasesAPIView._get_latest_refresh',
        return_value=ArtistsRefreshModel()
    )
    def test_get_from_spotify(self, artists_mock, spotify_mock, refresh_mock):
        session = self.client.session
        session['user_uuid'] = 'uuid'
        session.save()

        res = self.client.get('/api/artists')
        refresh_mock.assert_called()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
