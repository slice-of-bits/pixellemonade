from django.db import models


# Create your models here.

class ProductGroup(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()


class Product(models.Model):
    """
    source: https://www.prodigi.com/print-api/docs/reference/#product-details-object
    """
    of_group = models.ForeignKey('prodigi.ProductGroup', on_delete=models.CASCADE, related_name='products')
    sku = models.CharField(max_length=30, blank=None)
    description = models.CharField(max_length=120, null=True, blank=True)
    product_dimensions_height = models.PositiveSmallIntegerField(null=True, blank=True)
    product_dimensions_width = models.PositiveSmallIntegerField(null=True, blank=True)
    product_dimensions_unit = models.CharField(max_length=10, null=True, blank=True)
    attributes = models.JSONField(null=True, blank=True)

    price = models.DecimalField(max_digits=5, decimal_places=2)


class Recipient(models.Model):
    """
    source: https://www.prodigi.com/print-api/docs/reference/#order-object-recipient
    """
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address_line1 = models.CharField(max_length=200, null=False, blank=False)
    address_line2 = models.CharField(max_length=200, null=True, blank=True)
    address_postal_or_zip_code = models.CharField(max_length=50, null=False, blank=False)
    address_country_code = models.CharField(max_length=50, null=False, blank=False)
    address_town_or_city = models.CharField(max_length=200, null=False, blank=False)
    address_state_or_country = models.CharField(max_length=200, null=True, blank=True)


class Order(models.Model):
    """
    source: https://www.prodigi.com/print-api/docs/reference/#order-object
    """
    prodigi_id = models.CharField(max_length=30)
    created = models.DateTimeField()
    last_updated = models.DateTimeField()
    shipping_method = models.CharField(max_length=20)
    status = models.JSONField()
    charges = models.JSONField()
    shipments = models.JSONField()
    recipient = models.ForeignKey('prodigi.Recipient', on_delete=models.SET_NULL, null=True)


class OrderItem(models.Model):
    photo = models.ForeignKey('core.Photo', on_delete=models.SET_NULL, null=True)
    of_order = models.ForeignKey('prodigi.Order', related_name='items', on_delete=models.CASCADE)
    sku = models.CharField(max_length=30)
    copies = models.PositiveSmallIntegerField(default=1)
    sizing = models.CharField(max_length=20,
                              choices=[('fillPrintArea', 'fillPrintArea'), ('fitPrintArea', 'fitPrintArea'),
                                       ('stretchToPrintArea', 'stretchToPrintArea')])
    recipientCost = models.DecimalField(max_digits=5, decimal_places=2)
    attributes = models.JSONField()


class ShoppingCard(models.Model):
    pass


class ShoppingCardItem(models.Model):
    of_shopping_card = models.ForeignKey('prodigi.ShoppingCard', related_name='items', on_delete=models.CASCADE)
    photo = models.ForeignKey('core.Photo', on_delete=models.SET_NULL, null=True)
    count = models.PositiveSmallIntegerField(default=1)