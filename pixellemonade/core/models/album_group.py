from django.db import models


class AlbumGroup(models.Model):
    name = models.CharField(max_length=512, unique=True)