from pixellemonade.core.models import Photo
from celery import shared_task


@shared_task
def process_upload(photo_id):
    print(f"processing photo: {photo_id}")
    photo = Photo.objects.get(pk=photo_id)
    photo.make_thumbnails()
    photo.calculate_hash()
    photo.get_exif_data()
    photo.add_tags_based_on_iptc_tags()

    photo.save()