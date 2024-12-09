from django.db import models
from users.models import Buyer, Saleman

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    owner = models.ForeignKey(
        Saleman, on_delete=models.CASCADE, related_name="products", null=False
    )

    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)


class ProductBuyer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
