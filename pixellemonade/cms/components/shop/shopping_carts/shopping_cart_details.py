from django_unicorn.components import UnicornView
from pixellemonade.prodigi.models import ShoppingCard


class ShoppingCartDetailsView(UnicornView):
    cart = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.cart = ShoppingCard.objects.get(pk=kwargs.get('cart_id'))
