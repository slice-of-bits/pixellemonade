from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photo
from pixellemonade.prodigi.models import OrderItem, ProductGroup


class OrderingView(UnicornView):
    items = []
    product_groups = ProductGroup.objects.none()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        photos = Photo.objects.all().filter(pk__in=self.request.GET.get('ids').split(','))
        for photo in photos:
            self.items.append(OrderItem(photo=photo))

        self.product_groups = ProductGroup.objects.all()

    def remove_item(self, item_id):
        self.items.remove(item_id)

    def order_detail_count_plus(self, order_detail_id):
        pass

    def order_detail_count_minus(self, order_detail_id):
        pass
