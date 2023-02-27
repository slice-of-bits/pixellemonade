from django.urls import reverse
from django.test import TestCase, Client
from pixellemonade.core.models import Album, Photo


class TestPhotoEndpoint(TestCase):
    def setUp(self):
        self.client = Client()
        self.album1 = Album.objects.create(name='Test albums 1')
        self.photo = Photo.objects.create()
        self.response = self.client.get(reverse('api-1.0.0:photo_detail'))

    def test_photo_hash_included(self):
        self.assertContains(self.response, 'SOME-HASH')

    def test_photo_filename_included(self):
        self.assertContains(self.response, 'filename')

    def test_photo_small_thumbnail_included(self):
        self.assertContains(self.response, 'url')

    def test_photo_medium_thumbnail_included(self):
        self.assertContains(self.response, 'url')

    def test_photo_big_thumbnail_included(self):
        self.assertContains(self.response, 'url')

    def test_exif_data_included(self):
        self.assertContains(self.response, 'SOME-HASH')
