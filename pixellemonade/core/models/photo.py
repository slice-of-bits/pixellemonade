import hashlib
import os

from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from exif import Image
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from pixellemonade.core.storages import PrivateStorage, PublicStorage


def get_path(instance, filename):
    return 'albums/{0}/{1}'.format(instance.in_album.name, filename)


def get_small_thumbs_path(instance, filename):
    return 'thumbnails/{0}/small/{1}'.format(instance.in_album.name, filename)


def get_medium_thumbs_path(instance, filename):
    return 'thumbnails/{0}/medium/{1}'.format(instance.in_album.name, filename)


def get_big_thumbs_path(instance, filename):
    return 'thumbnails/{0}/big/{1}'.format(instance.in_album.name, filename)


class Photo(models.Model):
    image_hash = models.CharField(unique=True, max_length=64)
    original_image = models.ImageField(height_field='original_image_height',
                                       width_field='original_image_width',
                                       storage=PrivateStorage(), upload_to=get_path)
    original_image_height = models.PositiveIntegerField(null=True, blank=True)
    original_image_width = models.PositiveIntegerField(null=True, blank=True)
    tags = models.ManyToManyField('core.PhotoTag', name='tags')
    in_album = models.ForeignKey('core.Album', on_delete=models.CASCADE, blank=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    exif_shot_date_time = models.DateTimeField(blank=True, null=True, db_index=True)
    exif_json = models.JSONField(null=True)

    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    small_thumbnail_height = models.PositiveSmallIntegerField(null=True, blank=True)
    small_thumbnail_width = models.PositiveSmallIntegerField(null=True, blank=True)
    small_thumbnail = ProcessedImageField(upload_to=get_small_thumbs_path,
                                          processors=[ResizeToFit(500, 500)],
                                          format='JPEG',
                                          options={'quality': 60},
                                          height_field='small_thumbnail_height',
                                          width_field='small_thumbnail_width',
                                          null=True,
                                          storage=PublicStorage())

    medium_thumbnail_height = models.PositiveSmallIntegerField(null=True, blank=True)
    medium_thumbnail_width = models.PositiveSmallIntegerField(null=True, blank=True)
    medium_thumbnail = ProcessedImageField(upload_to=get_medium_thumbs_path,
                                           processors=[ResizeToFit(800, 800)],
                                           format='JPEG',
                                           options={'quality': 60},
                                           height_field='medium_thumbnail_height',
                                           width_field='medium_thumbnail_width',
                                           null=True,
                                           storage=PublicStorage())

    big_thumbnail_height = models.PositiveSmallIntegerField(null=True, blank=True)
    big_thumbnail_width = models.PositiveSmallIntegerField(null=True, blank=True)
    big_thumbnail = ProcessedImageField(upload_to=get_big_thumbs_path,
                                        processors=[ResizeToFit(3000, 3000)],
                                        format='JPEG',
                                        options={'quality': 85},
                                        height_field='big_thumbnail_height',
                                        width_field='big_thumbnail_width',
                                        null=True,
                                        storage=PublicStorage())

    @property
    def filename(self):
        return os.path.basename(self.original_image.name)

    def __str__(self):
        return self.original_image.name

    def calculate_hash(self):
        hash_md5 = hashlib.md5()
        with self.original_image.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        self.image_hash = hash_md5.hexdigest()

    def make_thumbnails(self):
        self.big_thumbnail.save(self.pk, self.original_image)
        self.medium_thumbnail.save(self.pk, self.original_image)
        self.small_thumbnail.save(self.pk, self.original_image)

    def get_exif_data(self):
        img_exif = Image(self.original_image.file)

        def get_flash_data(data):
            if data:
                return {"flash_fired": data.flash_fired}
            return None

        if img_exif.has_exif:
            self.exif_json = {
                'make': img_exif.get('make'),
                'model': img_exif.get('model'),
                'x_resolution': img_exif.get('x_resolution'),
                'y_resolution': img_exif.get('y_resolution'),
                'resolution_unit': img_exif.get('resolution_unit'),
                'software': img_exif.get('software'),
                'datetime': img_exif.get('datetime'),
                'artist': img_exif.get('artist'),
                'copyright': img_exif.get('copyright'),
                '_exif_ifd_pointer': img_exif.get('_exif_ifd_pointer'),
                'compression': img_exif.get('compression'),
                'jpeg_interchange_format': img_exif.get('jpeg_interchange_format'),
                'jpeg_interchange_format_length': img_exif.get('jpeg_interchange_format_length'),
                'exposure_time': img_exif.get('exposure_time'),
                'f_number': img_exif.get('f_number'),
                'exposure_program': img_exif.get('exposure_program'),
                'photographic_sensitivity': img_exif.get('photographic_sensitivity'),
                'sensitivity_type': img_exif.get('sensitivity_type'),
                'recommended_exposure_index': img_exif.get('recommended_exposure_index'),
                'exif_version': img_exif.get('exif_version'),
                'datetime_original': img_exif.get('datetime_original'),
                'datetime_digitized': img_exif.get('datetime_digitized'),
                'offset_time': img_exif.get('offset_time'),
                'offset_time_original': img_exif.get('offset_time_original'),
                'offset_time_digitized': img_exif.get('offset_time_digitized'),
                'shutter_speed_value': img_exif.get('shutter_speed_value'),
                'aperture_value': img_exif.get('aperture_value'),
                'brightness_value': img_exif.get('brightness_value'),
                'exposure_bias_value': img_exif.get('exposure_bias_value'),
                'max_aperture_value': img_exif.get('max_aperture_value'),
                'metering_mode': img_exif.get('metering_mode'),
                'light_source': img_exif.get('light_source'),
                'flash': get_flash_data(img_exif.get('flash')),
                'focal_length': img_exif.get('focal_length'),
                'color_space': img_exif.get('color_space'),
                'focal_plane_x_resolution': img_exif.get('focal_plane_x_resolution'),
                'focal_plane_y_resolution': img_exif.get('focal_plane_y_resolution'),
                'focal_plane_resolution_unit': img_exif.get('focal_plane_resolution_unit'),
                'file_source': img_exif.get('file_source'),
                'scene_type': img_exif.get('scene_type'),
                'custom_rendered': img_exif.get('custom_rendered'),
                'exposure_mode': img_exif.get('exposure_mode'),
                'white_balance': img_exif.get('white_balance'),
                'digital_zoom_ratio': img_exif.get('digital_zoom_ratio'),
                'focal_length_in_35mm_film': img_exif.get('focal_length_in_35mm_film'),
                'scene_capture_type': img_exif.get('scene_capture_type'),
                'contrast': img_exif.get('contrast'),
                'saturation': img_exif.get('saturation'),
                'sharpness': img_exif.get('sharpness'),
                'lens_specification': img_exif.get('lens_specification'),
                'lens_model': img_exif.get('lens_model'),
            }

            if img_exif.get('datetime_original'):
                self.exif_shot_date_time = img_exif.get('datetime_original', '').replace(':', '-', 2)


@receiver(models.signals.pre_delete, sender=Photo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Photo` object is deleted.
    """
    if instance.original_image:
        instance.original_image.delete()
    if instance.big_thumbnail:
        instance.big_thumbnail.delete()
    if instance.medium_thumbnail:
        instance.medium_thumbnail.delete()
    if instance.small_thumbnail:
        instance.small_thumbnail.delete()