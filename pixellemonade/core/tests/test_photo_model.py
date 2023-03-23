from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase
from pixellemonade.core.models import Photo, Album


class TestPhotoModel(TestCase):
    def setUp(self):
        self.album = Album.objects.create(name='Some test album')

    def get_test_file(self):
        return SimpleUploadedFile(name='Test image', content_type='image/jpeg',
                                  content=open(
                                      f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_1.jpg',
                                      'rb').read())

    def test_image_hash_generation(self):
        test_photo = Photo.objects.create(
            original_image=self.get_test_file(),
            in_album=self.album)
        test_photo.calculate_hash()

        self.assertEqual('2dfdd59b1164bdedc5d1a769e00fec44', test_photo.image_hash)

    def test_prevent_upload_the_same_image_using_hash(self):
        test_photo = Photo.objects.create(
            original_image=self.get_test_file(),
            in_album=self.album)
        test_photo.calculate_hash()
        test_photo.save()

        def add_a_double_image():
            test_photo_double = Photo.objects.create(
                original_image=self.get_test_file(),
                in_album=self.album)
            test_photo_double.calculate_hash()
            test_photo_double.save()

        self.assertRaises(IntegrityError, add_a_double_image)
