from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from pixellemonade.core.models import Album, Photo


class TestAnalytics(TestCase):
    def setUp(self):
        self.album = Album.objects.create(name='Some test album for analytics')
        self.photo = Photo.objects.create(in_album=self.album, original_image=SimpleUploadedFile(name='Test image',
                                                                                                 content_type='image/jpeg',
                                                                                                 content=open(
                                                                                                     f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_1.jpg',
                                                                                                     'rb').read()))
        self.photo.get_exif_data()
        self.photo.save()

    def test_view_redict_view(self):
        response = self.client.get(reverse('view_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(response.status_code, 302)

    def test_download_redirect_view(self):
        response = self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(response.status_code, 302)

    def test_getting_ip_from_request_from_HTTP_X_FORWARDED_FOR(self):
        response = self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}), HTTP_X_FORWARDED_FOR="1.2.3.4")
        self.photo.photoview_set.first().from_ip = "1.2.3.4"

    def test_getting_ip_from_request_from_REMOTE_ADDR(self):
        response = self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}),
                                   REMOTE_ADDR="1.2.3.4")
        self.photo.photoview_set.first().from_ip = "1.2.3.4"


class TestAlbumAnalytics(TestCase):
    def setUp(self):
        self.album = Album.objects.create(name='Some test album for analytics')
        self.photo = Photo.objects.create(in_album=self.album, original_image=SimpleUploadedFile(name='Test image',
                                                                                                 content_type='image/jpeg',
                                                                                                 content=open(
                                                                                                     f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_1.jpg',
                                                                                                     'rb').read()))
        self.photo.get_exif_data()
        self.photo.save()


class TestPhotoAnalytics(TestCase):
    def setUp(self):
        self.album = Album.objects.create(name='Some test album for photo analytics')
        self.photo = Photo.objects.create(in_album=self.album, original_image=SimpleUploadedFile(name='Test image',
                                                                                                 content_type='image/jpeg',
                                                                                                 content=open(
                                                                                                     f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_1.jpg',
                                                                                                     'rb').read()))
        self.photo.make_thumbnails()
        self.photo.save()

        self.client = Client(HTTP_X_FORWARDED_FOR="1.2.3.4", HTTP_USER_AGENT="Test User Agent")

    def test_photo_view_count(self):
        self.client.get(reverse('view_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(self.photo.view_count, 1)

    def test_photo_session_count(self):
        self.client.get(reverse('view_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(self.photo.session_count, 1)

    def test_photo_download_count(self):
        self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(self.photo.download_count, 1)
