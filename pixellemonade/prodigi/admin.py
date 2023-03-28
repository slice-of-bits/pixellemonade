from django.contrib import admin
from pixellemonade.prodigi.models import ProductGroup, Product, ShoppingCard


class ShoppingCardAdmin(admin.ModelAdmin):
    class Meta:
        model = ShoppingCard

# Register your models here.
admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(ShoppingCard)