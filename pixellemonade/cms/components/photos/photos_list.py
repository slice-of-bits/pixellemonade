from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photo, PhotoTag


class PhotosListView(UnicornView):
    photos = Photo.objects.none()
    search_input: str = None
    album_id = None
    limit = 50

    class Meta:
        javascript_exclude = ("photos", )  # this to prevent sending a lot of data to the browser

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.album_id = kwargs.get("album_id")
        self.search()

    def search(self):
        photos = Photo.objects.all()

        if self.album_id:
            photos = photos.filter(in_album__id=self.album_id)

        if self.search_input is not None and self.search_input != "None":
            print("searching")
            photos = photos.search(self.search_input)

        self.photos = photos[:self.limit]

    def updated_search_input(self, value):
        self.search()

    def load_more(self):
        self.limit += 20
        self.search()