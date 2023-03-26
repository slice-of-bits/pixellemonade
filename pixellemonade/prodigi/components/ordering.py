from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photo


class OrderingView(UnicornView):
    photos = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.photos = Photo.objects.all().filter(pk__in=self.request.GET.get('ids').split(','))
