from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photo


class TaggerView(UnicornView):
    tags: list = []
    current_photo: Photo = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.random_photo()

    def random_photo(self):
        self.current_photo = Photo.objects.all().first()

    def save_tags(self):
        self.current_photo.tags.add()
        self.random_photo()