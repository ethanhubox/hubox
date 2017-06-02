from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site

from cart.models import Cart
from django.contrib.auth.models import User
from ecommerce.models import Voucher, Course ,Vendor, AvailableTime


PAYMENT_CHOICE = (
    ('信用卡', '信用卡'),
    ('超商繳款', '超商繳款'),
)

class CourseOrder(models.Model):
    order_number = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    vendor = models.ForeignKey(Vendor)
    course = models.ForeignKey(Course)
    available_time = models.ForeignKey(AvailableTime)
    participants_number = models.PositiveIntegerField(default=1)
    voucher = models.ForeignKey(Voucher, null=True, blank=True)
    total_amount = models.PositiveIntegerField(default=0)
    payment_choice = models.CharField(max_length=20, choices=PAYMENT_CHOICE, blank=True)
    pay_check = models.BooleanField(default=False)
    eticket_send = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('course_order_detail', kwargs = {"pk": self.pk})

    class Meta:
        ordering = ['-pk',]


def course_order_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.pay_check:
        if instance.eticket_send == False:
            subject = "訂單成立"
            from_email = 'Hubox哈盒子'
            customer_mail = [instance.user.email,]
            ctx = {
                'course_order': instance,
                'host_name': Site.objects.get_current().domain
            }

            message = get_template('eticket.html').render(Context(ctx))
            msg = EmailMessage(subject, message, to=customer_mail, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()

            instance.eticket_send = True

pre_save.connect(course_order_pre_save_receiver, sender=CourseOrder)


def course_order_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.payment_choice:
        instance.available_time.quota -= instance.participants_number
        instance.available_time.save()

post_save.connect(course_order_post_save_receiver, sender=CourseOrder)

def course_order_pre_delete_receiver(sender, instance, *args, **kwargs):
    if instance.payment_choice:
        instance.available_time.quota += instance.participants_number
        instance.available_time.save()

pre_delete.connect(course_order_pre_delete_receiver, sender=CourseOrder)
