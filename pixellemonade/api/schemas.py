from datetime import datetime
from ninja import Schema


class AlbumOut(Schema):
    id: str
    title: str
    created_on: datetime
    photo_count: int = None

    def resolve_id(self, obj):
        return str(obj.pk)


class PhotoOut(Schema):
    id: str
    image_hash: str



    def resolve_id(self, obj):
        return str(obj.pk)
