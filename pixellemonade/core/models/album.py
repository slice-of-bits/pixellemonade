from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=512)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    groups = models.ManyToManyField('core.AlbumGroup', null=True, blank=True)

    @property
    def photo_count(self):
        return self.photo_set.all().count()

    @property
    def view_count(self):
        return self.photoview_set.objects.filter(of_album=self).count()

    @property
    def download_count(self):
        return self.photodownload_set.objects.filter(of_album=self).count()

    @property
    def session_count(self):
        return self.photoview_set.objects.filter(of_album=self).values('session_id').distinct().count()

    @property
    def thumbnail(self):
        return self.photo_set.first()

    def __str__(self):
        return self.name