from enum import Enum

from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db import models


# roles
class UserRole(Enum):
    SALEMAN = "saleman"
    BUYER = "buyer"

    @classmethod
    def choices(cls):
        return [(role.value, role.name.capitalize()) for role in cls]


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [(role.value, role.name.capitalize()) for role in UserRole]
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=16,
        choices=ROLE_CHOICES,
        default=UserRole.BUYER,
    )
    # defining required fields
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return self.username


class Saleman(models.Model):
    store_name = models.CharField(max_length=32)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Saleman: {self.user.last_name}"


class Buyer(models.Model):
    budget = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    purchased_products = models.ManyToManyField(
        "products.Product", through="products.ProductBuyer"
    )

    def __str__(self):
        return f"Buyer: {self.user.last_name}"
