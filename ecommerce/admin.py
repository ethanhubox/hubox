from django.contrib import admin
from django.db import models
from ghoster.admin import GhosterAdmin
from markdownx.widgets import AdminMarkdownxWidget
from .models import Vendor, Catagory, Course, AvailableTime, VendorMedia, CourseMedia, Material, Ordering, UserProfile, IndexEdit, IndexRole
# Register your models here.


class CourseInline(admin.TabularInline):
    model = Course

class AvailibleTimeInline(admin.TabularInline):
    model = AvailableTime

class VendorMediaInline(admin.TabularInline):
    model = VendorMedia

class CourseMediaInline(admin.TabularInline):
    model = CourseMedia

class IndexRoleInline(admin.TabularInline):
    model = IndexRole




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
    list_display = ('user', 'course', 'total_amount')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'phone', 'address')

class IndexEditAdmin(admin.ModelAdmin):
    inlines = [IndexRoleInline, ]
    list_display = ('title', 'photo', 'content',)

class IndexRoleAdmin(admin.ModelAdmin):
    list_display = ('order', 'mode',)

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Catagory, CatagoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(AvailableTime, AvailibleTimeAdmin)
admin.site.register(VendorMedia, VendorMediaAdmin)
admin.site.register(CourseMedia, CourseMediaAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Ordering, OderingAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(IndexEdit, IndexEditAdmin)
admin.site.register(IndexRole, IndexRoleAdmin)
