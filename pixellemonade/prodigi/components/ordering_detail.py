from django_unicorn.components import UnicornView
from pixellemonade.prodigi.models import ShoppingCardItem, ProductGroup, Product


class OrderingDetailView(UnicornView):
    detail = ShoppingCardItem.objects.none()
    selected_print_category = ProductGroup.objects.none()
    product_groups = None
    products = Product.objects.none()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.detail = kwargs.get("detail")
        self.product_groups = kwargs.get("product_groups")

    def order_detail_plus(self):
        self.detail.count += 1
        self.detail.save()

    def order_detail_minus(self):
        if self.detail.count > 1:
            self.detail.count -= 1
            self.detail.save()

    def updated_selected_print_category(self, value):
        self.products = Product.objects.filter(of_group_id=self.selected_print_category)

    def del_component(self):
        self.detail.delete()
        del self