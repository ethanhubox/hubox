from django.contrib import admin
from django.db import models
from ghoster.admin import GhosterAdmin
from markdownx.widgets import AdminMarkdownxWidget
from .models import Vendor, Catagory, Course, AvailableTime, VendorMedia, CourseMedia, Material, Ordering, UserProfile, UserSubscribe, IndexEdit, IndexRole, IndexVendor
# Register your models here.


class CourseInline(admin.StackedInline):
    model = Course
    extra = 0

class AvailibleTimeInline(admin.TabularInline):
    model = AvailableTime
    extra = 0

class VendorMediaInline(admin.TabularInline):
    model = VendorMedia
    extra = 0

class CourseMediaInline(admin.TabularInline):
    model = CourseMedia
    extra = 0

class IndexRoleInline(admin.TabularInline):
    model = IndexRole
    extra = 0

class IndexVendorInline(admin.StackedInline):
    model = IndexVendor
    extra = 0






class VendorAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }

    inlines = [VendorMediaInline, CourseInline, ]
    list_display = ('name',)

class CatagoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# class CourseAdmin(GhosterAdmin):
#
#     markdown_field = "introduce"
#     title_field = "name"
#
#     inlines = [AvailibleTimeInline, ]
#     list_display = ('vendor', 'name', 'catagory',)

class CourseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }

    inlines = [CourseMediaInline, AvailibleTimeInline, ]
    list_display = ('vendor', 'name', 'catagory',)

class AvailibleTimeAdmin(admin.ModelAdmin):
    list_display = ('course', 'date', 'start_time' ,'end_time' ,'quota')

class VendorMediaAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'file')

class CourseMediaAdmin(admin.ModelAdmin):
    list_display = ('course', 'file')

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('course', 'name', 'price')

class OderingAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('user', 'order_number')
    list_display = ('order_number', 'user', 'total_amount')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')

class UserSubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor')


class IndexEditAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }
    inlines = [IndexRoleInline, IndexVendorInline]
    list_display = ('name', 'photo', 'content',)

class IndexRoleAdmin(admin.ModelAdmin):
    list_display = ('order', 'mode',)

class IndexVendorAdmin(admin.ModelAdmin):
    list_display = ('order', 'vendor', )

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Catagory, CatagoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(AvailableTime, AvailibleTimeAdmin)
admin.site.register(VendorMedia, VendorMediaAdmin)
admin.site.register(CourseMedia, CourseMediaAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Ordering, OderingAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserSubscribe, UserSubscribeAdmin)
admin.site.register(IndexEdit, IndexEditAdmin)
admin.site.register(IndexRole, IndexRoleAdmin)
admin.site.register(IndexVendor, IndexVendorAdmin)
