from django_unicorn.components import UnicornView

from pixellemonade.core.models import Photo
from pixellemonade.prodigi.models import ShoppingCard, ProductGroup, ShoppingCardItem


class OrderingView(UnicornView):
    card = ShoppingCard.objects.none()
    items = []
    product_groups = ProductGroup.objects.none()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        # Check if the user already has a shopping card in the session
        if self.request.session.get('shopping_card_id'):
            try:
                self.card = ShoppingCard.objects.get(pk=self.request.session.get('shopping_card_id'))
            except ShoppingCard.DoesNotExist:
                self.card = ShoppingCard.objects.create()
                self.request.session['shopping_card_id'] = self.card.pk
        else:
            self.card = ShoppingCard.objects.create()
            self.request.session['shopping_card_id'] = self.card.pk

        photos = Photo.objects.all().filter(pk__in=self.request.GET.get('ids').split(','))
        for photo in photos:
            if not photo.pk in self.card.items.values_list('photo_id', flat=True):
                ShoppingCardItem.objects.create(photo=photo, of_shopping_card=self.card)

        self.product_groups = ProductGroup.objects.all()

    def add_detail(self, photo_id):
        item = ShoppingCardItem.objects.create(photo_id=photo_id, of_shopping_card=self.card)
        self.items.append(item)

    def remove_item(self, item_id):
        self.items.remove(item_id)

    def total_price(self):
        return sum([item.count * item.product.price for item in self.card.items.filter(product__isnull=False)])