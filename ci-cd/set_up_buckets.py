from minio import Minio

try:
    minio = Minio(
        's3:9000',
        access_key='user',
        secret_key='password',
        secure=False
    )
except Exception as ex:
    raise

minio.make_bucket('public')
minio.make_bucket('private')
print(f'{minio.list_buckets()}')
