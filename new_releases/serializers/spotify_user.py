from rest_framework import serializers

from new_releases.models import SpotifyUserModel


class SpotifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyUserModel
        fields = ['access_token', 'expires_in', 'refresh_token', 'user_uuid']
