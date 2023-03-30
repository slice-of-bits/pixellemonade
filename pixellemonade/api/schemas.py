from datetime import datetime
from ninja import Schema


class AlbumOut(Schema):
    id: str
    name: str
    created_on: datetime
    photo_count: int = None


class TagOut(Schema):
    name: str = None
    slug: str = None


class PhotoOut(Schema):
    id: str
    image_hash: str = None
    tags: list[TagOut]


class PhotoDetailsOut(Schema):
    id: str
    image_hash: str

    filename: str
    original_image: str
    original_image_height: int
    original_image_width: int
    tags: list[TagOut] = None

    uploaded_at: datetime
    exif_shot_date_time: datetime = None
    exif_json: dict = None
    owner: int = None

    small_thumbnail_height: int
    small_thumbnail_width: int
    small_thumbnail: str

    medium_thumbnail_height: int
    medium_thumbnail_width: int
    medium_thumbnail: str

    big_thumbnail_height: int
    big_thumbnail_width: int
    big_thumbnail: str


class AlbumDetailOut(Schema):
    id: str
    name: str
    created_on: datetime
    photo_count: int
    photo_set: list[PhotoOut]