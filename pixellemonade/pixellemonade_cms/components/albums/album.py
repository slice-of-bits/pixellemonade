from django_unicorn.components import UnicornView

from pixellemonade.core.models import Album


class AlbumView(UnicornView):
    _album: Album = None
    photos = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.album = Album.objects.get(pk=kwargs.get('album_id'))
        self.update_photos()

    def update_photos(self):
        self.photos = self.album.photo_set.all()