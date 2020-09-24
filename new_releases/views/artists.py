import logging
logger = logging.getLogger(__name__)

from django.shortcuts import redirect
from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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
        spotify_user = SpotifyUserModel.objects.get(user_uuid = request.session.get('user_uuid'))

        latest_refresh = None
        try:
            latest_refresh = ArtistsRefreshModel.objects.latest('date_refresh')
        except:
            pass

        artists = []
        if latest_refresh is None or latest_refresh.outdated:
            try:
                artists = self._refresh_artists(spotify_user)
            except Exception as e:
                raise e
        else:
            artists = ArtistModel.objects.all()

        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def _refresh_artists(self, spotify_user, tries = 0):
        try:
            artists = self.spotify_browse_service.retrieve_new_artists(
                spotify_user.access_token
            )
            return artists
        except HTTPError as e:
            if e.response.status_code == 401 and tries < 1:
                response = self.spotify_auth_service.refresh_auth(
                    spotify_user
                )
                spotify_user.access_token = response.get('access_token')
                spotify_user.save()
                tries += 1
                return self._refresh_artists(spotify_user, tries = tries)
            raise e

