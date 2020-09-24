from rest_framework import serializers

from new_releases.models import ImageModel


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = (
            'id',
            'url',
            'width',
            'height'
        )
