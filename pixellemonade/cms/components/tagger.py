from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photo, PhotoTag


class TaggerView(UnicornView):
    tags: list = []
    current_photo: Photo = None
    add_tag: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.random_photo()
        self.update_tags()

    def update_tags(self):
        self.tags = PhotoTag.objects.all()

    def random_photo(self):
        self.current_photo = Photo.objects.all().order_by('?')[0]

    def add_tag(self, tag_id):
        self.current_photo.tags.add(tag_id)

    def add_new_tag(self):
        PhotoTag.objects.create(name=self.add_tag, created_by=self.request.user)
        self.update_tags()

    def remove_tag(self, tag_id):
        self.current_photo.tags.remove(tag_id)
