from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField


class Photographer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=128)
    instagram = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    flickr = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    profile_description = models.TextField(null=True, blank=True)
    copyright_match = ArrayField(models.CharField(max_length=64), null=True, blank=True)

    @property
    def photo_count(self):
        return self.photo_set.count()

    def __str__(self):
        return self.full_name
