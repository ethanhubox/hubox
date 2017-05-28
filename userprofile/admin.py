from django.contrib import admin

from .models import Profile, Subscribe
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name',)

class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
