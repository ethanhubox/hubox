from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete

from django.contrib.auth.models import User
from ecommerce.models import AvailableTime
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user)

    def update_total(self):
        total = 0
        for item in CartItem.objects.filter(cart=self):
            total += item.item_total
        self.total = total
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart)
    available_time = models.ForeignKey(AvailableTime)
    participants_number = models.PositiveIntegerField(default=1)
    item_total = models.PositiveIntegerField()

    def __str__(self):
        return str(self.available_time)

def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    course_price = instance.available_time.course.price
    participants_number = instance.participants_number
    instance.item_total = int(course_price) * int(participants_number)

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_total()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)

def cart_item_post_delete_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_total()

post_delete.connect(cart_item_post_delete_receiver, sender=CartItem)
