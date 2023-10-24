import hashlib
import os
import re

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
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


class PhotoManager(models.Manager):
    def search(self, query):
        queryset = self.all()
        PhotoTag = apps.get_model('core', 'PhotoTag')

        # Check if the input contains search options
        if ":" in query:
            # Get all search options using regex
            search_option = re.findall(r'(\w+:[\w\s-]*)(?!\w*:)', query)
            # Get all tags using regex
            tags_input = re.findall(r'[\w\s]+(?!\w*:)', query)[0]

            # If the input only contains search options, set tags_input to empty string
            # @todo this could be done better
            if ":" in query.split(' ')[0]:
                tags_input = ''

            # Loop through all search options and filter the queryset
            for option in search_option:
                if option.startswith('album'):
                    queryset = queryset.filter(in_album__name__icontains=option.split(':')[1])
                elif option.startswith('order_by'):
                    queryset = queryset.order_by(option.split(':')[1])
                elif option.startswith('orientation'):
                    if option.split(':')[1] == 'horizontal':
                        queryset = queryset.filter(original_image_height__lt=models.F('original_image_width'))
                    elif option.split(':')[1] == 'vertical':
                        queryset = queryset.filter(original_image_height__gt=models.F('original_image_width'))
                    elif option.split(':')[1] == 'square':
                        queryset = queryset.filter(original_image_height=models.F('original_image_width'))
                else:
                    raise ValueError(f'Unknown search option {option}')

            # Loop through all tags and filter the queryset
            if len(tags_input) > 1:
                for tag_str in tags_input.split():
                    tag = PhotoTag.objects.filter(name__icontains=tag_str)
                    queryset = queryset.filter(tags__in=tag)

        else:
            # If no search options are given, search for tags and order by date
            if len(query) > 1:
                tags = PhotoTag.objects.filter(name__icontains=query)
                queryset = queryset.filter(tags__in=tags)
            else:
                queryset = queryset.order_by('-exif_shot_date_time')

        return queryset


class Photo(models.Model):
    image_hash = models.CharField(unique=True, max_length=64, null=True)
    photographer = models.ForeignKey('core.Photographer', on_delete=models.SET_NULL, null=True)
    original_image = models.ImageField(height_field='original_image_height',
                                       width_field='original_image_width',
                                       storage=PrivateStorage(), upload_to=get_path)
    original_image_height = models.PositiveIntegerField(null=True, blank=True)
    original_image_width = models.PositiveIntegerField(null=True, blank=True)
    tags = models.ManyToManyField('core.PhotoTag', name='tags', null=True, blank=True)
    in_album = models.ForeignKey('core.Album', on_delete=models.CASCADE, blank=False, related_name='photos')

    uploaded_at = models.DateTimeField(auto_now_add=True)
    exif_shot_date_time = models.DateTimeField(blank=True, null=True, db_index=True)
    exif_json = models.JSONField(null=True)

    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

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

    objects = PhotoManager()

    @property
    def view_count(self):
        return self.photoview_set.all().count()

    @property
    def view_session_count(self):
        return self.photoview_set.distinct('session').count()

    @property
    def download_count(self):
        return self.photodownload_set.all().count()

    @property
    def download_session_count(self):
        return self.photodownload_set.distinct('session').count()

    @property
    def big_thumbnail_download_url(self):
        return self.big_thumbnail.storage.url(self.filename, parameters={
            'ResponseContentDisposition': f'attachment; filename={self.filename}',
        })

    @property
    def original_image_download_url(self):
        return self.original_image.storage.url(self.original_image.name, parameters={
            'ResponseContentDisposition': f'attachment; filename={self.filename}',
        })

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
        # Open the original image
        content = self.original_image.read()
        # Loop through the processed image fields
        for field in [self.small_thumbnail, self.medium_thumbnail, self.big_thumbnail]:
            # Save the processed image to the desired location using the storage argument
            field.save(f'{self.original_image.name}.jpg', ContentFile(content))

    def add_tags_based_on_iptc_tags(self):
        from iptcinfo3 import IPTCInfo

        info = IPTCInfo(self.original_image)

        for k in info['keywords']:
            iptc_tag = str(k.decode('UTF-8')).rstrip('\0')
            tag, created = apps.get_model('core', 'PhotoTag').objects.get_or_create(name=iptc_tag)
            self.tags.add(tag)

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
        else:
            print('No exif found')

        if self.exif_json.get('copyright'):
            Photographer = apps.get_model('core', 'Photographer')

            photographer = Photographer.objects.filter(copyright_match__contains=[self.exif_json.get('copyright')])
            if photographer.exists():
                self.photographer = photographer.first()


    @property
    def style_width(self):
        return int(self.original_image_width * 280 / self.original_image_height)

    @property
    def flex_grow(self):
        return int(self.original_image_width * 280 / self.original_image_height)

    @property
    def padding_bottom(self):
        return int(self.original_image_height / self.original_image_width * 100)


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
