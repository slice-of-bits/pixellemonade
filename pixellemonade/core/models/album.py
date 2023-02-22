from django.db import models

from pixellemonade.core.models.photo import Photo
from pixellemonade.core.models.album_group import AlbumGroup


class Album(models.Model):
    title = models.CharField(max_length=512)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    photos = models.ManyToManyField(Photo)
    groups = models.ManyToManyField(AlbumGroup)

    @property
    def hash_id_str(self):
        return str(self.pk)