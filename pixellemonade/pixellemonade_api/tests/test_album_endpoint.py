import json

from django.test import TestCase, Client
from django.urls import reverse

from pixellemonade.core.models import AlbumGroup, Album


class TestAlbumEndpoint(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_album_group = AlbumGroup.objects.create(name='Test album group 1', slug='test-album-group-1')
        self.test_album_group2 = AlbumGroup.objects.create(name='Test album group 2', slug='test-album-group-2')

        self.test_album = Album.objects.create(name='Test album 1',)

    def test_get_album_title(self):
        """Test that the album title is returned"""
        res = self.client.get(reverse('api-1.0.0:get_album', kwargs={'album_id': self.test_album.pk}))
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.json().get('name'), 'Test album 1')

    def test_get_album_photo_count(self):
        """Test that the album photo count is returned"""
        res = self.client.get(reverse('api-1.0.0:get_album', kwargs={'album_id': self.test_album.pk}))
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.json().get('photo_count'), 0)

    def test_can_not_create_album_without_name(self):
        """Test that an album can not be created without a name"""
        res = self.client.post(reverse('api-1.0.0:create_album'), {"name": ""})
        self.assertEquals(res.status_code, 400)

    def test_create_album(self):
        """Test that an album can be created"""
        res = self.client.post(reverse('api-1.0.0:create_album'), json.dumps({"name": "Test album 1"}),
                               content_type='application/json')
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.json().get('name'), 'Test album 1')

    def test_create_album_with_groups(self):
        """Test that an album can be created with groups"""
        res = self.client.post(reverse('api-1.0.0:create_album'), json.dumps(
            {"name": "Test album 1", "groups": [self.test_album_group.pk, self.test_album_group2.pk]}),
                               content_type='application/json')
        self.assertEquals(res.status_code, 200)
        self.assertEquals(len(res.json().get('groups')), 2)
