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
        self.photo.make_thumbnails()
        self.photo.save()

    def test_view_redict_view(self):
        response = self.client.get(reverse('view_photo', kwargs={'id': self.photo.pk, 'size': 'small'}))
        self.assertEqual(response.status_code, 302)

    def test_download_redirect_view(self):
        response = self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}),
                                   HTTP_USER_AGENT="Test User Agent")
        self.assertEqual(response.status_code, 302)

    def test_getting_ip_from_request_from_HTTP_X_FORWARDED_FOR(self):
        response = self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}),
                                   HTTP_X_FORWARDED_FOR="1.2.3.4", HTTP_USER_AGENT="Test User Agent")
        self.photo.photodownload_set.all().first().from_ip = "1.2.3.4"

    def test_getting_ip_from_request_from_REMOTE_ADDR(self):
        response = self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}),
                                   REMOTE_ADDR="1.2.3.4", HTTP_USER_AGENT="Test User Agent")
        self.photo.photodownload_set.all().first().from_ip = "1.2.3.4"


class TestPhotoViewAnalytics(TestCase):
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

    def test_photo_view_count_is_one_after_first_view(self):
        self.client.get(reverse('view_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(self.photo.view_count, 1)

    def test_photo_view_session_count_is_one_after_first_view(self):
        self.client.get(reverse('view_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(self.photo.view_session_count, 1)

    def test_photo_view_session_count_is_one_after_multiple_from_the_same_session(self):
        self.client.get(reverse('view_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.client.get(reverse('view_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.client.get(reverse('view_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(self.photo.view_session_count, 1)

    def test_photo_view_session_count_is_two_after_multiple_from_different_sessions(self):
        self.client.get(reverse('view_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.client.session.clear()
        self.client.get(reverse('view_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(self.photo.view_session_count, 2)


class TestPhotoDownloadAnalytics(TestCase):
    def setUp(self):
        self.album = Album.objects.create(name='Some test album for download tests')
        self.photo = Photo.objects.create(in_album=self.album, original_image=SimpleUploadedFile(name='Test image',
                                                                                                 content_type='image/jpeg',
                                                                                                 content=open(
                                                                                                     f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_1.jpg',
                                                                                                     'rb').read()))
        self.photo.make_thumbnails()
        self.photo.save()

        self.client = Client(HTTP_X_FORWARDED_FOR="1.2.3.4", HTTP_USER_AGENT="Test User Agent")

    def test_photo_download_count_is_one_after_first_view(self):
        self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(self.photo.download_count, 1)

    def test_photo_download_session_count_is_one_after_first_view(self):
        self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(self.photo.download_session_count, 1)

    def test_photo_download_session_count_is_one_after_multiple_from_the_same_session(self):
        self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(self.photo.download_session_count, 1)

    def test_photo_download_session_count_is_two_after_multiple_from_different_sessions(self):
        self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.client.session.clear()
        self.client.get(reverse('download_photo', kwargs={'id': self.photo.pk, 'size': 'big'}))
        self.assertEqual(self.photo.download_session_count, 2)
