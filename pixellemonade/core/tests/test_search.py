from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from pixellemonade.core.models import Photo, Album, PhotoTag


class TestPhotoSearch(TestCase):
    def setUp(self):
        self.album1 = Album.objects.create(name='Some test album 1')
        self.album2 = Album.objects.create(name='photo album 2')
        self.photo1 = Photo.objects.create(in_album=self.album1,
                                          original_image=SimpleUploadedFile(name='Test image',
                                                                            content_type='image/jpeg',
                                                                            content=open(
                                                                                f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_1.jpg',
                                                                                'rb').read()))
        self.photo2 = Photo.objects.create(in_album=self.album2,
                                          original_image=SimpleUploadedFile(name='Test image',
                                                                            content_type='image/jpeg',
                                                                            content=open(
                                                                                f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_2.jpg',
                                                                                'rb').read()))
        self.photo1.get_exif_data()
        self.photo1.save()

        self.photo2.get_exif_data()
        self.photo2.save()

    def test_search_by_tag_returns_photo_all_photos_when_input_is_empty(self):
        photos = Photo.objects.search('')
        self.assertEqual(2, photos.count())

    def test_only_return_photo_from_album(self):
        photos = Photo.objects.search('album: Some test album 1')
        self.assertEqual(1, photos.count())

    def test_only_return_photos_that_have_tag(self):
        tag = PhotoTag.objects.create(name='banana')
        self.photo1.tags.add(tag)
        result = Photo.objects.search('banana')
        self.assertEqual(1, result.count())
        self.assertEqual(self.photo1, result[0])
