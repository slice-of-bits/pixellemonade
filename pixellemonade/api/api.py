from typing import List
from ninja import NinjaAPI

from pixellemonade.api.schemas import AlbumOut, PhotoOut
from pixellemonade.core.models import Album, Photo

api = NinjaAPI()


@api.get("/albums", response=List[AlbumOut])
def albums_list(request):
    return Album.objects.all()


@api.get("/photos", response=List[PhotoOut])
def photos_list(request):
    return Photo.objects.all()


@api.get("/album/{album_id}/photos", response=List[PhotoOut])
def photos_list(request, album_id):
    return Album.objects.get(pk=album_id).photos.all()
