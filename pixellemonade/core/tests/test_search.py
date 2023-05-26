from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from pixellemonade.core.models import Photo, Album, PhotoTag


class TestPhotoSearch(TestCase):
    def setUp(self):
        self.album1 = Album.objects.create(name='Some test album 1')
        self.album2 = Album.objects.create(name='cool pictures')
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
        self.photo3 = Photo.objects.create(in_album=self.album2,
                                          original_image=SimpleUploadedFile(name='Test image',
                                                                            content_type='image/jpeg',
                                                                            content=open(
                                                                                f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_2.jpg',
                                                                                'rb').read()))
        self.photo1.get_exif_data()
        self.photo1.save()

        self.photo2.get_exif_data()
        self.photo2.save()

        self.photo3.get_exif_data()
        self.photo3.save()

    def test_search_by_tag_returns_photo_all_photos_when_input_is_empty(self):
        photos = Photo.objects.search('')
        self.assertEqual(3, photos.count())

    def test_only_return_photo_from_album(self):
        photos = Photo.objects.search('album:cool pictures')
        self.assertEqual(2, photos.count())

    def test_only_return_photos_that_have_tag(self):
        tag = PhotoTag.objects.create(name='banana')
        self.photo1.tags.add(tag)
        result = Photo.objects.search('banana')
        self.assertEqual(1, result.count())
        self.assertEqual(self.photo1, result[0])

    def test_order_by_search_operator_on_date(self):
        result = Photo.objects.search('order_by:exif_shot_date_time')
        self.assertEqual(self.photo1, result.first())
        self.assertEqual(self.photo3, result.last())

    def test_order_by_search_operator_on_date_reverse(self):
        result = Photo.objects.search('order_by:-exif_shot_date_time')
        self.assertEqual(self.photo3, result.first())
        self.assertEqual(self.photo1, result.last())

    def test_use_order_by_and_album_together(self):
        result = Photo.objects.search('album:Some test album 1 order_by:-exif_shot_date_time')
        self.assertEqual(self.photo1, result.first())
        self.assertEqual(self.photo1, result.last())

    def test_use_order_by_and_tag_together(self):
        tag = PhotoTag.objects.create(name='banana')
        self.photo1.tags.add(tag)
        self.photo2.tags.add(tag)
        result = Photo.objects.search('banana order_by:-exif_shot_date_time')
        print(result)
        self.assertEqual(self.photo2, result.first())
        self.assertEqual(self.photo1, result.last())