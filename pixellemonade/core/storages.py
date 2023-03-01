from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class PublicStorage(S3Boto3Storage):
    access_key = settings.PUBLIC_S3_ACCESS_KEY
    secret_key = settings.PUBLIC_S3_SECRET_KEY
    endpoint_url = settings.PRIVATE_S3_ENDPOINT_URL

    bucket_name = settings.PUBLIC_S3_BUCKET_NAME
    custom_domain = settings.PUBLIC_S3_CUSTOM_DOMAIN_NAME
    querystring_auth = True


class PrivateStorage(S3Boto3Storage):
    access_key = settings.PRIVATE_S3_ACCESS_KEY
    secret_key = settings.PRIVATE_S3_SECRET_KEY
    endpoint_url = settings.PRIVATE_S3_ENDPOINT_URL

    bucket_name = settings.PRIVATE_S3_BUCKET_NAME
    custom_domain = settings.PRIVATE_S3_CUSTOM_DOMAIN_NAME
    querystring_auth = False