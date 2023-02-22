from django_unicorn.components import UnicornView

from pixellemonade.core.models import Album


class AlbumView(UnicornView):
    album: Album = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.album = Album.objects.get(pk=kwargs.get('album_id'))

    def photos(self):
        return self.album.photos.all()
