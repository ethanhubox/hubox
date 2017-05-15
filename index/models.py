from django.db import models

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
