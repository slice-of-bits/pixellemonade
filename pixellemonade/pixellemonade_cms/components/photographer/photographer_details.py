from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photographer


class PhotographerDetailsView(UnicornView):
    photographer = Photographer.objects.none()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.photographer = kwargs.get('photographer')

    def save(self):
        self.photographer.save()
        self.photographer = Photographer.objects.get(pk=self.photographer.pk)
        self.reset()

