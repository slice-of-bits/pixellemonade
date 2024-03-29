from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from pixellemonade.core.models import Album, Photo


class TestExifDataExtraction(TestCase):
    def setUp(self):
        self.album = Album.objects.create(name='Some test album')
        self.photo = Photo.objects.create(in_album=self.album, original_image=SimpleUploadedFile(name='Test image', content_type='image/jpeg',
                                       content=open(
                                           f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_1.jpg', 'rb').read()))
        self.photo.get_exif_data()
        self.photo.save()

    def test_get_exif_camera_model(self):
        self.assertEqual(self.photo.exif_json.get('model'), 'Some Test Camera')

    def test_get_exif_camera_manufacturer(self):
        self.assertTrue(self.photo.exif_json.get('make'), 'Test Camera BV')
