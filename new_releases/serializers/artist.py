from rest_framework import serializers

from new_releases.models import ArtistModel
from .genre import GenreSerializer
from .image import ImageSerializer


class ArtistSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    images = ImageSerializer(
        source='imagemodel_set',
        many=True
    )

    class Meta:
        model = ArtistModel
        fields = (
            'id',
            'spotify_id',
            'name',
            'followers',
            'genres',
            'images',
            'popularity'
        )
