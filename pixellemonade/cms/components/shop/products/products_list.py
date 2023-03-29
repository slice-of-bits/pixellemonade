from django_unicorn.components import UnicornView

from pixellemonade.prodigi.models import Product


class ProductsListView(UnicornView):
    products = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.products = Product.objects.all()
