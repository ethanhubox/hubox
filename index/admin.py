from django.contrib import admin

from .models import IndexPage, IndexBanner
# Register your models here.

class IndexBannerInline(admin.TabularInline):
    model = IndexBanner
    extra = 0


class IndexPageAdmin(admin.ModelAdmin):
    inlines = [IndexBannerInline, ]
    list_display = ('name',)

class IndexBannerAdmin(admin.ModelAdmin):
    list_display = ('index', 'banner')

admin.site.register(IndexPage, IndexPageAdmin)
admin.site.register(IndexBanner, IndexBannerAdmin)
