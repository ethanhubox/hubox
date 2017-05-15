from django.contrib import admin
from django.db import models
from markdownx.widgets import AdminMarkdownxWidget
from .models import IndexPage, IndexBanner, MemberTerms, PrivacyPolicy, CatagoryPage, FAQ
# Register your models here.

# class IndexBannerInline(admin.TabularInline):
#     model = IndexBanner
#     extra = 0
#
#
# class IndexPageAdmin(admin.ModelAdmin):
#     inlines = [IndexBannerInline, ]
#     list_display = ('name',)
#
# class IndexBannerAdmin(admin.ModelAdmin):
#     list_display = ('index', 'banner')


class MemberTermsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }
    list_display = ('terms', )

class PrivacyPolicyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }
    list_display = ('policy', )

class FAQAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }
    list_display = ('faq', )

class CatagoryPageAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }
    list_display = ('title', )

# admin.site.register(IndexPage, IndexPageAdmin)
# admin.site.register(IndexBanner, IndexBannerAdmin)
admin.site.register(MemberTerms, MemberTermsAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(CatagoryPage, CatagoryPageAdmin)
