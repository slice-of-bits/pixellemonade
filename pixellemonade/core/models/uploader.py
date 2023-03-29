from django.db import models
from django.contrib.auth import get_user_model


class Uploader(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    full_name = models.CharField(max_length=128)
    instagram_profile = models.URLField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    flickr_profile = models.URLField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    profile_description = models.TextField()

    def __str__(self):
        return self.full_name
