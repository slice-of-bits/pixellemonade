from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from pixellemonade.core.models import Album, Photo


class TestShoppingCart(TestCase):
    def setUp(self):
        self.test_album = Album.objects.create(name='Test albums 1')
        self.test_photo = Photo.objects.create(in_album=self.test_album,
                                               original_image=SimpleUploadedFile(name='Test image',
                                                                                 content_type='image/jpeg',
                                                                                 content=open(
                                                                                     f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_1.jpg',
                                                                                     'rb').read()))

        user = get_user_model().objects.create_user(username='testuser', password='testpassword')

        client = Client()
        client.force_login(user)

    def test_create_new_shoppingcart_when_no_session_found(self):
        pass
