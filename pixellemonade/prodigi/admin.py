from django.contrib import admin
from pixellemonade.prodigi.models import ProductGroup, Product, ShoppingCard


class ShoppingCardAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'products_count']

    class Meta:
        model = ShoppingCard


# Register your models here.
admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(ShoppingCard, ShoppingCardAdmin)
