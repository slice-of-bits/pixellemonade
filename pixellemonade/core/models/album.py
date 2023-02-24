from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=512)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    groups = models.ManyToManyField('core.AlbumGroup')

    @property
    def hash_id_str(self):
        return str(self.pk)

    def __str__(self):
        return self.name