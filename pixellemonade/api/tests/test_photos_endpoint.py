from django.urls import reverse
from django.test import TestCase, Client
from pixellemonade.core.models import Album, AlbumGroup


class TestPhotosEndpoint(TestCase):
    def setUp(self):
        self.client = Client()
        self.album1 = Album.objects.create(name='Test albums 1')

    def test_photo_hash_included(self):
        response = self.client.get()

    def test_tags_search(self):
        response = self.client.get()