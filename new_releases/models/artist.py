from django.db import models

from .abstract_model import AbstractBaseModel
from .genre import GenreModel


class ArtistModel(AbstractBaseModel):
    spotify_id = models.CharField(max_length=256, null=False, unique=True)
    name = models.CharField(max_length=256, null=False)
    followers = models.IntegerField()
    popularity = models.IntegerField()
    genres = models.ManyToManyField(GenreModel, blank=True)

    def __str__(self):
        return f"""<Artist
            spotify_id={self.spotify_id}
            name={self.name}
            followers={self.followers}
            popularity={self.popularity}
            genres={self.genres}
        >"""
