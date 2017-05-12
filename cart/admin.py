from django.contrib import admin

from .models import Cart, CartItem
# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline, ]
    list_display = ('user',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'available_time')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
