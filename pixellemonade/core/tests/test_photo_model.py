from django.test import TestCase
from pixellemonade.core.models.photo import Photo


class TestPhotoModel(TestCase):

    def test_image_hash_is_generated(self):
        test_photo = Photo.objects.create()
        expexted_hash = ''
        self.assertEqual(expexted_hash, test_photo.image_hash)

    def test_prevent_upload_the_same_image_using_hash(self):
        test_photo = Photo.objects.create()

        def add_a_double_image():
            test_photo2 = Photo.objects.create()

        self.assertRaises(SomeCoolException, add_a_double_image)
