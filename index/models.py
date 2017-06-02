from django.db import models

from ecommerce.models import Vendor

# Create your models here.
class IndexPage(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

def index_media(instance, filename):
    return "index/banner/{}".format(filename)

class IndexBanner(models.Model):
    index = models.ForeignKey(IndexPage)
    banner = models.FileField(upload_to=index_media)

    def __str__(self):
        return str(self.banner)



class IndexVendorRole(models.Model):
    index = models.ForeignKey(IndexPage)
    order = models.IntegerField(unique=True)
    vendor = models.ForeignKey(Vendor)

    def __str__(self):
        return self.vendor.name

    class Meta:
        ordering = ['order',]







class MemberTerms(models.Model):
    terms = models.TextField()

    def __str__(self):
        return str(self.pk)

class PrivacyPolicy(models.Model):
    policy = models.TextField()

    def __str__(self):
        return str(self.pk)

class FAQ(models.Model):
    faq = models.TextField()

    def __str__(self):
        return str(self.pk)

def catagory_page_media(instance, filename):
    return "catagory/banner/{}".format(filename)

class CatagoryPage(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    banner = models.FileField(upload_to=catagory_page_media)

    def __str__(self):
        return str(self.pk)
