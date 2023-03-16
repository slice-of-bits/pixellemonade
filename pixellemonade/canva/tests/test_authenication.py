import json

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from pixellemonade.core.models import Album, Photo
from pixellemonade.core.tasks import process_upload
from pixellemonade.canva.models import CanvaUser


class TestCanvaAuthentication(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(
            email='admin@email.com',
            password='adminpassword123',
            username='admin'
        )
        self.album = Album.objects.create(name='Test albums 1')
        self.photo = Photo.objects.create(in_album=self.album,
                                          original_image=SimpleUploadedFile(
                                              name='Test image',
                                              content_type='image/jpeg',
                                              content=open(
                                                  f'{settings.BASE_DIR}\\core\\tests\\test_images\\test_image_1.jpg',
                                                  'rb').read()))
        process_upload(self.photo.id)

    def test_canva_user_id_not_found_returns_body_with_error(self):
        body = {"user": "SOME_USER_ID", "brand": "string", "label": "string", "limit": 0, "type": "string",
                "locale": "string", "query": "string"}
        response = self.client.post(reverse('canva_api:canva_find'), json.dumps(body), content_type="application/json")
        self.assertEqual(response.json().get("type"), "ERROR")
        self.assertEqual(response.json().get("errorCode"), "CONFIGURATION_REQUIRED")

    def test_canva_user_id_is_found_returns_body_with_no_error(self):
        CanvaUser.objects.create(canva_user_id='SOME_USER_ID', user=self.user)
        body = {"user": "SOME_USER_ID", "brand": "string", "label": "string", "limit": 0, "type": "string",
                "locale": "string", "query": "string"}
        response = self.client.post(reverse('canva_api:canva_find'), json.dumps(body), content_type="application/json")
        self.assertNotEqual(response.json().get("type"), "ERROR")
        self.assertNotEqual(response.json().get("errorCode"), "CONFIGURATION_REQUIRED")


    def test_canva_user_id_is_added_if_user_is_authenticated(self):
        self.client.force_login(self.user)
        res = self.client.post(f"{reverse('canva_login')}?user=123456&state=09876")
        self.assertEqual(res.status_code, 200)
        canva_user = CanvaUser.objects.get(canva_user_id='123456')
        self.assertEqual(canva_user.canva_user_id, '123456')

    def test_canva_user_id_is_not_added_if_user_is_not_authenticated(self):
        res = self.client.post(f"{reverse('canva_login')}?user=123456&state=09876")
        self.assertEqual(res.status_code, 302)
        canva_user = CanvaUser.objects.filter(canva_user_id='123456')
        self.assertTrue(canva_user.exists())
