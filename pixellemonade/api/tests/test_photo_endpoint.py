import urllib.parse

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from pixellemonade.core.models import Album, Photo
from pixellemonade.core.tasks import process_upload


class TestPhotoEndpoint(TestCase):
    def setUp(self):
        self.client = Client()
        self.album = Album.objects.create(name='Test albums 1')
        self.photo = Photo.objects.create(in_album=self.album,
                                          original_image=SimpleUploadedFile(
                                              name='Test image',
                                              content_type='image/jpeg',
                                              content=open(
                                                  f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_1.jpg',
                                                  'rb').read()))
        process_upload(self.photo.id)
        self.response = self.client.get(reverse('api-1.0.0:photo_detail', kwargs={'photo_id': self.photo.id}))

    def test_photo_hash_included(self):
        self.assertContains(self.response, '2dfdd59b1164bdedc5d1a769e00fec44')

    def test_photo_filename_included(self):
        self.assertIn('Test_image', self.response.json().get('filename'))

    def test_photo_small_thumbnail_included(self):
        self.assertTrue(
            f'thumbnails/{urllib.parse.quote(self.album.name)}/small/{self.photo.id}'
            in self.response.json().get('small_thumbnail'))

    def test_photo_medium_thumbnail_included(self):
        self.assertTrue(
            f'thumbnails/{urllib.parse.quote(self.album.name)}/medium/{self.photo.id}'
            in self.response.json().get('medium_thumbnail'))

    def test_photo_big_thumbnail_included(self):
        self.assertTrue(
            f'thumbnails/{urllib.parse.quote(self.album.name)}/big/{self.photo.id}'
            in self.response.json().get('big_thumbnail'))
