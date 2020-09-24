from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from new_releases.models import SpotifyUserModel
from new_releases.services.spotify import (
    SpotifyAuthAPIService,
    SpotifyTokenRequestInvalidException,
)
from new_releases.serializers import (
    SpotifyUserSerializer,
)


class AbstractBaseAuthAPIView(APIView):
    def __init__(self):
        self.spotify_service = SpotifyAuthAPIService()


class AuthAPIView(AbstractBaseAuthAPIView):
    def get(self, request):
        r = self.spotify_service.get_user()
        return redirect(r)


class AuthCallbackAPIView(AbstractBaseAuthAPIView):
    def get(self, request):
        try:
            raw_spotify_user = self.spotify_service.get_user_token(
                request.query_params.get('code')
            )
            spotify_user = SpotifyUserModel(**raw_spotify_user)
            spotify_user.save()

            request.session['user_uuid'] = str(spotify_user.user_uuid)
            serializer = SpotifyUserSerializer(spotify_user)
            return Response(serializer.data)
        except SpotifyTokenRequestInvalidException:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
