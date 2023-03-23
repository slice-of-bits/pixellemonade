from datetime import datetime, timedelta

from django.urls import reverse
from django.test import TestCase, Client
from pixellemonade.core.models import Album, AlbumGroup


class TestAlbumsEndpoint(TestCase):
    def setUp(self):
        self.client = Client()

        self.album1 = Album.objects.create(name='Test albums 1')
        self.album2 = Album.objects.create(name='Test albums 2')
        self.album3 = Album.objects.create(name='Test albums 3')

        self.group1 = AlbumGroup.objects.create(name='private', slug='private')

    def test_get_all_albums(self):
        response = self.client.get(reverse('api-1.0.0:albums_list'))
        self.assertContains(response, self.album1.name)
        self.assertContains(response, self.album2.name)
        self.assertContains(response, self.album3.name)

    def test_get_all_albums_in_album_group(self):
        self.album1.groups.add(self.group1)

        response = self.client.get(f"{reverse('api-1.0.0:albums_list')}?groups={self.group1.slug}")
        self.assertContains(response, self.album1.name)
        self.assertNotContains(response, self.album2.name)
        self.assertNotContains(response, self.album3.name)

    def test_album_ordered_by_date_created(self):
        response = self.client.get(f"{reverse('api-1.0.0:albums_list')}")
        print(response.json())
        self.assertEqual(response.json()[0]['name'], self.album3.name)

        self.album1.created_on = datetime.now() + timedelta(days=1)
        self.album1.save()

        response = self.client.get(f"{reverse('api-1.0.0:albums_list')}")

        self.assertEqual(response.json()[0]['name'], self.album1.name)
        self.assertEqual(response.json()[1]['name'], self.album3.name)


