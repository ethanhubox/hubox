from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cart, name='cart'),
    url(r'^check_out$', views.check_out, name='check_out'),
    url(r'^cart_item_count$', views.cart_item_count, name='cart_item_count'),
]
