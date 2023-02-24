import os
from storages.backends.s3boto3 import S3Boto3Storage
from tempfile import SpooledTemporaryFile
from django.conf import settings

class CustomS3Boto3Storage:
    pass


class PrivateStorage(S3Boto3Storage):
    access_key = 'xU46FM88poL0GsvB'
    secret_key = '0I0oQJWThsDHUqH7hNzlwzcKCv6xVwbx'
    endpoint_url = settings.S3_URL

    bucket_name = 'private'
    custom_domain = ''
    querystring_auth = True


class PublicStorage(S3Boto3Storage):
    access_key = 'xU46FM88poL0GsvB'
    secret_key = '0I0oQJWThsDHUqH7hNzlwzcKCv6xVwbx'
    endpoint_url = settings.S3_URL

    bucket_name = 'public'
    custom_domain = ''
    querystring_auth = False