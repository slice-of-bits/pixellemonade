from django_unicorn.components import UnicornView
from pixellemonade.prodigi.models import ShoppingCardItem, Product


class OrderingDetailView(UnicornView):
    detail = ShoppingCardItem.objects.none()
    selected_product_group_id = None
    selected_print_product_id = None
    product_groups = None
    products = Product.objects.none()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.detail = kwargs.get("detail")
        self.product_groups = kwargs.get("product_groups")

        # If the detail has a product, we need to set the selected product group and product
        if self.detail.product:
            self.selected_product_group_id = self.detail.product.of_group_id
            self.updated_selected_product_group_id(self.selected_product_group_id)

            self.selected_print_product_id = self.detail.product.pk

    # fot the plus button
    def order_detail_plus(self):
        self.detail.count += 1
        self.detail.save()

    # for the minus button
    def order_detail_minus(self):
        if self.detail.count > 1:
            self.detail.count -= 1
            self.detail.save()

    # get the product in the selected product_group
    def updated_selected_product_group_id(self, value):
        self.products = Product.objects.filter(of_group_id=self.selected_product_group_id)

    # when a product is selected, set the detail product to the selected product and save it to the database
    def updated_selected_print_product_id(self, value):
        self.detail.product = Product.objects.get(pk=self.selected_print_product_id)
        self.detail.save()

    # delete the detail and the component
    def del_component(self):
        self.detail.delete()
        del self

    def duplicate_photo(self):
        self.parent.add_detail(self.detail.photo.pk)

    def total_price(self):
        if self.detail.product:
            return self.detail.count * self.detail.product.price
        else:
            return 0