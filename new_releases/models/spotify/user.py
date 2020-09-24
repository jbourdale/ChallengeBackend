import uuid
from django.db import models

from new_releases.models.abstract_model import AbstractBaseModel


class SpotifyUserModel(AbstractBaseModel):
    access_token = models.CharField(max_length=255, blank=False, null=False)
    token_type = models.CharField(max_length=255, blank=False, null=False)
    expires_in = models.IntegerField(null=True, blank=False)
    scope = models.CharField(max_length=255, blank=False, null=False)
    refresh_token = models.CharField(max_length=255, blank=False, null=False)
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"""<SpotifyUser
            access_token={self.access_token}
            expires_in={self.expires_in}
            refresh_token={self.refresh_token}
            uuid={self.user_uuid}
        >"""
