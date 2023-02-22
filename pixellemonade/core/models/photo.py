import hashlib

from django.db import models
from imagekit.models import ProcessedImageField
from django.contrib.auth import get_user_model
from pilkit.processors import ResizeToFit


def get_path(instance, filename):
    return 'albums/{0}/{1}'.format(instance.of_album.name, filename)


def get_small_thumbs_path(instance, filename):
    return 'thumbnails/{0}/small/{1}'.format(instance.of_album.name, filename)


def get_medium_thumbs_path(instance, filename):
    return 'thumbnails/{0}/medium/{1}'.format(instance.of_album.name, filename)


def get_big_thumbs_path(instance, filename):
    return 'thumbnails/{0}/big/{1}'.format(instance.of_album.name, filename)


class Photo(models.Model):
    image_hash = models.CharField(unique=True, max_length=64)
    original_image = models.ImageField(height_field='original_image_height',
                                       width_field='original_image_width')
    original_image_height = models.PositiveIntegerField(null=True, blank=True)
    original_image_width = models.PositiveIntegerField(null=True, blank=True)

    uploaded_at = models.DateTimeField()
    exif_shot_date_time = models.DateTimeField(db_index=True)
    exif_rating = models.PositiveSmallIntegerField(default=0, db_index=True)
    exif_fstop = models.FloatField(blank=True, null=True)
    exif_focal_length = models.FloatField(blank=True, null=True)
    exif_iso = models.IntegerField(blank=True, null=True)
    exif_shutter_speed = models.TextField(blank=True, null=True)
    exif_camera = models.TextField(blank=True, null=True)
    exif_lens = models.TextField(blank=True, null=True)

    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    small_thumbnail_height = models.PositiveSmallIntegerField(null=True, blank=True)
    small_thumbnail_width = models.PositiveSmallIntegerField(null=True, blank=True)
    small_thumbnail = ProcessedImageField(upload_to=get_small_thumbs_path,
                                          processors=[ResizeToFit(500, 500)],
                                          format='JPEG',
                                          options={'quality': 60},
                                          height_field='small_thumbnail_height',
                                          width_field='small_thumbnail_width',
                                          null=True)

    medium_thumbnail_height = models.PositiveSmallIntegerField(null=True, blank=True)
    medium_thumbnail_width = models.PositiveSmallIntegerField(null=True, blank=True)
    medium_thumbnail = ProcessedImageField(upload_to=get_medium_thumbs_path,
                                           processors=[ResizeToFit(800, 800)],
                                           format='JPEG',
                                           options={'quality': 60},
                                           height_field='medium_thumbnail_height',
                                           width_field='medium_thumbnail_width',
                                           null=True)

    big_thumbnail_height = models.PositiveSmallIntegerField(null=True, blank=True)
    big_thumbnail_width = models.PositiveSmallIntegerField(null=True, blank=True)
    big_thumbnail = ProcessedImageField(upload_to=get_big_thumbs_path,
                                        processors=[ResizeToFit(3000, 3000)],
                                        format='JPEG',
                                        options={'quality': 85},
                                        height_field='big_thumbnail_height',
                                        width_field='big_thumbnail_width',
                                        null=True)

    def calculate_hash(self):
        hash_md5 = hashlib.md5()
        with self.original_image as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        self.image_hash = hash_md5.hexdigest()

