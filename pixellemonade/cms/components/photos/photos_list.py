from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photo


class PhotosListView(UnicornView):
    photos = Photo.objects.all()
    search_input: str = None

    def search(self):
        print(f'Search for: {self.search_input}')
        photos = Photo.objects.all()
        if self.search_input:
            photos = photos.filter(tags__name__contains=self.search_input)

        self.photos = photos

    def updated_search_input(self, value):
        self.search()