from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photo, PhotoTag


class PhotosListView(UnicornView):
    photos = None
    search_input: str = None
    album_id = None
    tags = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.album_id = kwargs.get("album_id")
        self.search()

    def search(self):
        photos = Photo.objects.all()
        if self.album_id:
            print(self.album_id)
            photos = photos.filter(in_album=self.album_id)

        if self.search_input:
            self.tags = PhotoTag.objects.all().filter(name__icontains=self.search_input)
            photos = photos.filter(tags__in=self.tags)
        self.photos = photos

    def updated_search_input(self, value):
        self.search()