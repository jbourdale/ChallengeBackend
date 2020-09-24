from rest_framework import serializers

from new_releases.models import GenreModel


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreModel
        fields = ('id', 'name')
