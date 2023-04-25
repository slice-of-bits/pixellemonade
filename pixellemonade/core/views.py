from django.shortcuts import redirect
from pixellemonade.core.models import Photo, PhotoView


# Create your views here.

def view_photo(request, id, size):
    photo = Photo.objects.get(pk=id)

    p = PhotoView(photo_id=photo.pk, photo_size=size, of_album=photo.in_album)
    p.process_request(request)
    p.save()

    return redirect(photo.__getattribute__(f"{size}_thumbnail").url)


def download_photo(request, id, size):
    photo = Photo.objects.get(pk=id)

    p = PhotoView(photo_id=photo.pk, photo_size=size, of_album=photo.in_album)
    p.process_request(request)
    p.save()

    return redirect(photo.original_image_download_url)
