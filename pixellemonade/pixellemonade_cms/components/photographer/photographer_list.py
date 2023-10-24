from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photographer


class PhotographerListView(UnicornView):
    photographers = Photographer.objects.none()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.photographers = Photographer.objects.all()


