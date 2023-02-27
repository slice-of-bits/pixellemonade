from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=512)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    groups = models.ManyToManyField('core.AlbumGroup', null=True, blank=True)

    @property
    def photo_count(self):
        return self.photo_set.all().count()

    def __str__(self):
        return self.name