from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from pixellemonade.core.models import Photo, Album, PhotoTag


class TestPhotoSearch(TestCase):
    def setUp(self):
        self.album1 = Album.objects.create(name='Some test album 1')
        self.album2 = Album.objects.create(name='cool pictures')

        self.photo2 = Photo.objects.create(in_album=self.album2,
                                           original_image=SimpleUploadedFile(name='Test image',
                                                                             content_type='image/jpeg',
                                                                             content=open(
                                                                                 f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_2.jpg',
                                                                                 'rb').read()))

        self.photo_horizontal = Photo.objects.create(in_album=self.album1,
                                                     original_image=SimpleUploadedFile(name='Horizontal image',
                                                                                       content_type='image/jpeg',
                                                                                       content=open(
                                                                                           f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_horizontal.jpg',
                                                                                           'rb').read()))

        self.photo_vertical = Photo.objects.create(in_album=self.album2,
                                                   original_image=SimpleUploadedFile(name='Vertical image',
                                                                                     content_type='image/jpeg',
                                                                                     content=open(
                                                                                         f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_vertical.jpg',
                                                                                         'rb').read()))

        self.photo2.get_exif_data()
        self.photo2.save()

        self.photo_horizontal.get_exif_data()
        self.photo_horizontal.save()

        self.photo_vertical.get_exif_data()
        self.photo_vertical.save()

    def test_search_by_tag_returns_photo_all_photos_when_input_is_empty(self):
        photos = Photo.objects.search('')
        self.assertEqual(3, photos.count())

    def test_only_return_photo_from_album(self):
        photos = Photo.objects.search('album:cool pictures')
        self.assertEqual(2, photos.count())

    def test_only_return_photos_that_have_tag(self):
        tag = PhotoTag.objects.create(name='banana')
        self.photo_horizontal.tags.add(tag)
        result = Photo.objects.search('banana')
        self.assertEqual(1, result.count())
        self.assertEqual(self.photo_horizontal, result[0])

    def test_order_by_search_operator_on_date(self):
        result = Photo.objects.search('order_by:exif_shot_date_time')
        self.assertEqual(self.photo_horizontal, result.first())
        self.assertEqual(self.photo_vertical, result.last())

    def test_order_by_search_operator_on_date_reverse(self):
        result = Photo.objects.search('order_by:-exif_shot_date_time')
        self.assertEqual(self.photo_vertical, result.first())
        self.assertEqual(self.photo_horizontal, result.last())

    def test_use_order_by_and_album_together(self):
        result = Photo.objects.search('album:Some test album 1 order_by:-exif_shot_date_time')
        self.assertEqual(self.photo_horizontal, result.first())
        self.assertEqual(self.photo_horizontal, result.last())

    def test_use_order_by_and_tag_together(self):
        tag = PhotoTag.objects.create(name='banana')
        self.photo_horizontal.tags.add(tag)
        self.photo2.tags.add(tag)
        result = Photo.objects.search('banana order_by:-exif_shot_date_time')
        self.assertEqual(self.photo2, result.first())
        self.assertEqual(self.photo_horizontal, result.last())

    def test_filter_by_orientation_horizontal(self):
        result = Photo.objects.search('orientation:horizontal')
        print(result)
        self.assertEqual(result.first(), self.photo_horizontal)
        self.assertEqual(result.count(), 1)

    def test_filter_by_orientation_square(self):
        result = Photo.objects.search('orientation:square')
        self.assertEqual(result.count(), 1)

    def test_filter_by_orientation_vertical(self):
        result = Photo.objects.search('orientation:vertical')
        self.assertEqual(result.first(), self.photo_vertical)
        self.assertEqual(result.count(), 1)