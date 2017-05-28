from django.db import models

from django.contrib.auth.models import User
from ecommerce.models import Vendor
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=200)

    def __str__(self):
        return str(self.user)


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['user',]
