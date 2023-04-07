from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from pixellemonade.core.models import Album, Photo


class TestPhotosEndpoint(TestCase):
    def setUp(self):
        self.client = Client()
        self.album1 = Album.objects.create(name='Test albums 1')
        self.photo1 = Photo.objects.create(in_album=self.album1,
                                           original_image=SimpleUploadedFile(
                                               name='Test image 1',
                                               content_type='image/jpeg',
                                               content=open(
                                                   f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_1.jpg',
                                                   'rb').read()))
        self.photo2 = Photo.objects.create(in_album=self.album1,
                                           original_image=SimpleUploadedFile(
                                               name='Test image 2',
                                               content_type='image/jpeg',
                                               content=open(
                                                   f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_2.jpg',
                                                   'rb').read()))
        self.photo3 = Photo.objects.create(in_album=self.album1,
                                           original_image=SimpleUploadedFile(
                                               name='Test image 3',
                                               content_type='image/jpeg',
                                               content=open(
                                                   f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_3.jpg',
                                                   'rb').read()))

    def test_photo_hashid_included(self):
        response = self.client.get(reverse('api-1.0.0:photos_list'))
        self.assertEquals(response.status_code, 200)

    def test_tags_search(self):
        response = self.client.get(reverse('api-1.0.0:photos_list'))
        self.assertEquals(response.status_code, 200)
