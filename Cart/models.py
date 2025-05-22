from django.db import models
from Authentication.models import CustomUser
from ShipShopHome.models import Product

# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
