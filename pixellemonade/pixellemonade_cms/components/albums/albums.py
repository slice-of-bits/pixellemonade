from django_unicorn.components import UnicornView
from pixellemonade.core.models.album import Album


class AlbumsView(UnicornView):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required

    def albums(self):
        return Album.objects.all()

    def delete(self, album_id):
        Album.objects.get(pk=album_id).delete()
        self.albums()
