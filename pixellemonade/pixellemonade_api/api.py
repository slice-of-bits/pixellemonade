from datetime import datetime
from typing import List

from ninja import NinjaAPI, Schema
from ninja.files import UploadedFile

from pixellemonade.core.models import Album, Photo
from pixellemonade.core.tasks import process_upload
from pixellemonade.pixellemonade_api.schemas import AlbumOut, PhotoOut, PhotoDetailsOut, AlbumDetailOut, AlbumIn

api = NinjaAPI()


@api.get("/photos", response=List[PhotoOut], url_name='photos_list')
def photos_list(request):
    return Photo.objects.all()[:100]


@api.get("/photo/{photo_id}", response=PhotoDetailsOut, url_name='photo_detail')
def photos_list(request, photo_id):
    return Photo.objects.get(pk=photo_id)


@api.get("/albums", response=List[AlbumOut], url_name='albums_list')
def albums_list(request, groups: str = None):
    albums = Album.objects.all().order_by('-created_on')
    if groups:
        groups_list = groups.split(',')
        albums = albums.filter(groups__slug__in=groups_list)
    return albums


@api.post("/album", response=AlbumOut, url_name='create_album')
def create_album(request, albumin: AlbumIn):
    album = Album.objects.create(name=albumin.name)
    if albumin.groups:
        album.groups.add(*albumin.groups)
    return album


@api.get("/album/{album_id}", response=AlbumDetailOut, url_name='get_album')
def album_details(request, album_id):
    return Album.objects.get(pk=album_id)


@api.post("/album/{album_id}/upload/")
def photo_upload(request, album_id, file: UploadedFile, process_now: bool = False):
    photo = Photo(original_image=file, in_album_id=album_id)
    photo.save()
    if request.POST.get('process_now', False):
        photo.make_thumbnails()
        photo.calculate_hash()
        photo.get_exif_data()
        photo.add_tags_based_on_iptc_tags()
        processing = 'Done'
    else:
        process_upload.delay(photo.id)
        processing = "queued"
    return {'name': file.name,
            'processing': processing}





