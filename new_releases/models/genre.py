from django.db import models

from .abstract_model import AbstractBaseModel


class GenreModel(AbstractBaseModel):
    name = models.CharField(max_length=256, null=False, unique=True)

    def __repr__(self):
       return f'<Genre name={self.name}>'

