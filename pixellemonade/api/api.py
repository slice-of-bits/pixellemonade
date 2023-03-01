from typing import List
from ninja import NinjaAPI
from ninja.files import UploadedFile

from pixellemonade.api.schemas import AlbumOut, PhotoOut, PhotoDetailsOut, AlbumDetailOut, PhotoCanvaOut, \
    PhotoCanvaSearchIn
from pixellemonade.core.models import Album, Photo
from pixellemonade.core.tasks import process_upload

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


@api.get("/photo/{photo_id}", response=PhotoDetailsOut, url_name='photo_detail')
def photos_list(request, photo_id):
    return Photo.objects.get(pk=photo_id)


@api.get("/album/{album_id}", response=AlbumDetailOut)
def album_details(request, album_id):
    return Album.objects.get(pk=album_id)


@api.post("/album/{album_id}/upload")
def photo_upload(request, album_id, file: UploadedFile):
    photo = Photo(original_image=file, in_album_id=album_id)
    # photo.calculate_hash()
    photo.save()
    process_upload.delay(photo.id)
    return {'name': file.name}


@api.post("/content/resources/find",)
def canva_resources_find(request, body: PhotoCanvaSearchIn):
    photos = Photo.objects.all()
    if body.query:
        photos = photos.filter(tags__name__contains=body.query)

    response_json = {
        "type": "SUCCESS",
        "resources": [PhotoCanvaOut.from_orm(i).dict() for i in photos]
    }

    return response_json

