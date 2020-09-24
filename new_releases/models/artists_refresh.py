import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings

from .abstract_model import AbstractBaseModel
from .genre import GenreModel


class ArtistsRefreshModel(AbstractBaseModel):
    date_refresh = models.DateTimeField(auto_now_add=True)

    @property
    def outdated(self):
        refresh_valid_timedelta = datetime.timedelta(seconds = settings.SPOTIFY_ARTISTS_REFRESH_INTERVAL)
        expires_at = timezone.now() + refresh_valid_timedelta
        print("date_refresh : " + str(self.date_refresh))
        print("expires at : " + str(timezone.now() + refresh_valid_timedelta))
        return expires_at < self.date_refresh

    def __repr__(self):
        return f"<ArtistRefreshModel date_refresh={self.date_refresh}>"
