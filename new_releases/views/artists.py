import datetime

from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from new_releases.serializers import ArtistSerializer
from new_releases.models import (
    ArtistsRefreshModel,
    SpotifyUserModel,
    ArtistModel
)
from new_releases.services.spotify import (
    SpotifyAuthAPIService,
    SpotifyBrowseAPIService
)


class ArtistReleasesAPIView(APIView):
    def __init__(self):
        self.spotify_browse_service = SpotifyBrowseAPIService()
        self.spotify_auth_service = SpotifyAuthAPIService()

    def get(self, request):
        if not request.session.get('user_uuid'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        spotify_user = SpotifyUserModel.objects.get(
            user_uuid=request.session.get('user_uuid')
        )
        if spotify_user is None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        latest_refresh = self._get_latest_refresh()

        try:
            artists = self._get_artists(spotify_user, latest_refresh)
        except Exception as e:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def _get_artists(self, spotify_user, latest_refresh):
        artists = []
        if latest_refresh is None or latest_refresh.outdated:
            artists = self._refresh_artists(spotify_user)
        else:
            artists = ArtistModel.objects.all()
        return artists

    def _get_latest_refresh(self):
        try:
            latest_refresh = ArtistsRefreshModel.objects.latest('date_refresh')
        except Exception:
            return None
        return latest_refresh

    def _refresh_artists(self, spotify_user, tries=0):
        datetime_token_refresh_at = (
            spotify_user.created_at +
            datetime.timedelta(seconds=spotify_user.expires_in * 0.75)
        )

        if (datetime_token_refresh_at > timezone.now()):
            response = self.spotify_auth_service.refresh_auth(
                spotify_user
            )
            spotify_user.access_token = response.get('access_token')
            spotify_user.save()

        artists = self.spotify_browse_service.retrieve_new_artists(
            spotify_user.access_token
        )
        return artists
