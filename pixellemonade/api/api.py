from typing import List
from ninja import NinjaAPI
from ninja.files import UploadedFile

from pixellemonade.api.schemas import AlbumOut, PhotoOut, PhotoDetailsOut, AlbumDetailOut
from pixellemonade.core.models import Album, Photo

api = NinjaAPI()


@api.get("/albums", response=List[AlbumOut], url_name='albums_list')
def albums_list(request, groups: str = None):
    albums = Album.objects.all()
    if groups:
        groups_list = groups.split(',')
        albums = albums.filter(groups__slug__in=groups_list)
    return albums


@api.get("/photos", response=List[PhotoOut])
def photos_list(request):
    return Photo.objects.all()[:100]


@api.get("/photo/{album_id}", response=PhotoDetailsOut, url_name='photo_detail')
def photos_list(request, photo_id):
    return Photo.objects.get(pk=photo_id)


@api.get("/album/{album_id}", response=AlbumDetailOut)
def album_details(request, album_id):
    return Album.objects.get(pk=album_id)


@api.post("/album/{album_id}/upload")
def photo_upload(request, album_id, file: UploadedFile):
    photo = Photo(original_image=file, image_hash=file.name, in_album_id=album_id)
    # photo.calculate_hash()
    photo.save()
    return {'name': file.name}
