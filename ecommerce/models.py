from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.core.mail import send_mail
from django.conf import settings
# Create your models here.

def vendor_logo(instance, filename):
    ext = filename.split('.')[-1]
    return "{}/{}大頭貼.{}".format(instance.name, instance.name, ext)
def vendor_banner(instance, filename):
    ext = filename.split('.')[-1]
    return "{}/{}封面照片.{}".format(instance.name, instance.name, ext)

class Vendor(models.Model):
    name = models.CharField(max_length=50)
    story = models.TextField()

    catagory = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=vendor_logo)
    banner = models.ImageField(upload_to=vendor_banner)
    video = models.CharField(max_length=200)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    subscribe_number = models.PositiveIntegerField()


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vendor_detail', kwargs={'pk':self.pk})



VENDOE_POSITION_CHOISES = (
('剪影', '剪影'),
('故事', '故事'),
)

def vendor_media(instance, filename):
    return "{}/{}/{}".format(instance.vendor.name, instance.position, filename)

class VendorMedia(models.Model):
    vendor = models.ForeignKey(Vendor)
    order = models.IntegerField()
    position = models.CharField(max_length=50, choices=VENDOE_POSITION_CHOISES)
    file = models.FileField(upload_to=vendor_media)

    def __str__(self):
        return str(self.file)

    class Meta:
        ordering = ['vendor', 'position', 'order']


def catagory_upload(instance, filename):
    ext = filename.split('.')[-1]
    return "catagory/{}.{}".format(instance.name, ext)

class Catagory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=catagory_upload)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    introduce = models.TextField()

    vendor = models.ForeignKey(Vendor)
    catagory = models.ForeignKey(Catagory)
    content = models.TextField()
    course_durations = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=100)
    bus = models.CharField(max_length=100)
    mrt = models.CharField(max_length=100)
    minmum_number = models.IntegerField()
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk':self.pk})

    class Meta:
        ordering = ['vendor',]

def course_media(instance, filename):
    return "{}/media/{}".format(instance.course.name, filename)

class CourseMedia(models.Model):
    course = models.ForeignKey(Course)
    order = models.IntegerField()
    file = models.FileField(upload_to=course_media)

    def __str__(self):
        return str(self.file)
    class Meta:
        ordering = ['course', 'order']

class Material(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name + " +TWD " + str(self.price)


class AvailableTime(models.Model):
    course = models.ForeignKey(Course)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    quota = models.IntegerField()
    format_date = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.date.strftime("%m月%d日 （%a.）") + self.start_time.strftime("%H:%M～") + self.end_time.strftime("%H:%M") + " 剩餘" + str(self.quota) + "人"

    class Meta:
        ordering = ['course', 'date', 'start_time']

def available_time_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.format_date = instance.date.strftime("%m月%d日")

pre_save.connect(available_time_pre_save_receiver, sender=AvailableTime)


class Ordering(models.Model):
    user = models.ForeignKey(User)
    vendor = models.ForeignKey(Vendor)
    course = models.ForeignKey(Course)
    material = models.ForeignKey(Material, null=True, blank=True)
    available_time = models.ForeignKey(AvailableTime)
    participants_number = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField()
    check_value = models.CharField(max_length=500)
    payment = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('ordering_detail', kwargs = {"pk": self.pk})

def ordering_post_save_receiver(sender, instance, *args, **kwargs):
    available_time = instance.available_time
    available_time.quota -= instance.participants_number
    available_time.save()


    # message = "感謝您購買" + instance.course.name + "課程<br>您選擇的素材為：" + instance.material.name + "<br>上課時間為：" + str(instance.available_time)
    # send_mail("hi", "miwooro@hotmail.com", ["miwooro@hotmail.com"], html_message=message)

post_save.connect(ordering_post_save_receiver, sender=Ordering)

def ordering_post_delete_receiver(sender, instance, *args, **kwargs):
    available_time = instance.available_time
    available_time.quota += instance.participants_number
    available_time.save()

post_delete.connect(ordering_post_delete_receiver, sender=Ordering)


GENDER_CHOICE = (
    ('男', '男'),
    ('女', '女'),
    ('不願透露', '不願透露'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=200)

    def __str__(self):
        return str(self.user)


class UserSubscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['user',]


def index_media(instance, filename):
    return "index/{}".format(filename)

class IndexEdit(models.Model):
    name = models.CharField(max_length=50)
    photo = models.FileField(upload_to=index_media)
    content = models.TextField()
    more = models.URLField()
    vendor_more = models.URLField()

    def __str__(self):
        return self.name

MODE_CHOICE = (
    ('隨機', '隨機'),
    ('指定分類', '指定分類'),
    ('特定課程', '特定課程'),
)

class IndexRole(models.Model):
    index_edit = models.ForeignKey(IndexEdit)
    order = models.IntegerField(unique=True)
    name = models.CharField(max_length=50, blank=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICE)
    catagory = models.ForeignKey(Catagory, blank=True, null=True)
    course = models.ManyToManyField(Course, blank=True)
    more = models.URLField()

    def __str__(self):
        return str(self.order)

    class Meta:
        ordering = ['order',]

class IndexVendor(models.Model):
    index_edit = models.ForeignKey(IndexEdit)
    order = models.IntegerField(unique=True)
    vendor = models.ForeignKey(Vendor)

    def __str__(self):
        return self.vendor.name

    class Meta:
        ordering = ['order',]
