from django.db import models


class PhotoTag(models.Model):
    name = models.CharField(max_length=128)
    created_on = models.DateTimeField()
    created_by = models.DateTimeField()