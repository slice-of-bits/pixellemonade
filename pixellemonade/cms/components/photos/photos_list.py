from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photo, PhotoTag


class PhotosListView(UnicornView):
    photos = None
    search_input: str = None
    album_id = None

    class Meta:
        javascript_exclude = ("photos", )  # this to prevent sending a lot of data to the browser

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.album_id = kwargs.get("album_id")
        self.search()

    def search(self):
        photos = Photo.objects.all().prefetch_related('tags')
        if self.album_id:
            photos = photos.filter(in_album=self.album_id)

        if self.search_input:
            photos = Photo.objects.all().filter(tags__name__contains=self.search_input).distinct('pk').prefetch_related('tags')
        self.photos = photos

    def updated_search_input(self, value):
        self.search()