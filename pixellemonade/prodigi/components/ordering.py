from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photo
from pixellemonade.prodigi.models import ShoppingCard, ProductGroup, ShoppingCardItem


class OrderingView(UnicornView):
    card = ShoppingCard.objects.none()
    items = []
    product_groups = ProductGroup.objects.none()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        if self.request.session.get('shopping_card_id'):
            self.card = ShoppingCard.objects.get(pk=self.request.session.get('shopping_card_id'))
        else:
            self.card = ShoppingCard.objects.create()
            self.request.session['shopping_card_id'] = self.card.pk

        photos = Photo.objects.all().filter(pk__in=self.request.GET.get('ids').split(','))
        for photo in photos:
            if not photo.pk in self.card.items.values_list('photo_id', flat=True):
                ShoppingCardItem.objects.create(photo=photo, of_shopping_card=self.card)

        self.product_groups = ProductGroup.objects.all()

    def remove_item(self, item_id):
        self.items.remove(item_id)

    def order_detail_count_plus(self, order_detail_id):
        pass

    def order_detail_count_minus(self, order_detail_id):
        pass
