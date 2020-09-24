from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

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
            user_uui=request.session.get('user_uuid')
        )
        if spotify_user is None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        latest_refresh = self._get_latest_refresh()
        artists = self._get_artists(spotify_user, latest_refresh)

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
        except:
            return None
        return latest_refresh

    def _refresh_artists(self, spotify_user, tries=0):
        try:
            artists = self.spotify_browse_service.retrieve_new_artists(
                spotify_user.access_token
            )
            return artists
        except HTTPError as e:
            if (
                e.response.status_code == status.HTTP_401_UNAUTHORIZED and
                tries < 1
            ):
                response = self.spotify_auth_service.refresh_auth(
                    spotify_user
                )
                spotify_user.access_token = response.get('access_token')
                spotify_user.save()
                tries += 1
                return self._refresh_artists(spotify_user, tries=tries)
            raise e
