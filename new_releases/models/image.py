from django.db import models

from .abstract_model import AbstractBaseModel
from .artist import ArtistModel


class ImageModel(AbstractBaseModel):
    artist = models.ForeignKey(ArtistModel, on_delete=models.CASCADE)
    url = models.URLField(null=False)
    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)

    def __repr__(self):
        return f"""<Image
            url={self.url}
            width={self.width}
            height={self.height}
        >"""
