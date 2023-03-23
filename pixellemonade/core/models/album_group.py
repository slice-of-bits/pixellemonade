from django.db import models


class AlbumGroup(models.Model):
    name = models.CharField(max_length=512, unique=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name