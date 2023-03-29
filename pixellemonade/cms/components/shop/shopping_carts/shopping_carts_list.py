from django_unicorn.components import UnicornView
from pixellemonade.prodigi.models import ShoppingCard


class ShoppingCartsListView(UnicornView):
    carts = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.carts = ShoppingCard.objects.all()
