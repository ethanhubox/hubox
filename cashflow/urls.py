from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add_merchant$', views.add_merchant, name='add_merchant'),
    url(r'^payment$', views.payment, name='payment'),
    url(r'^finish_order/$', views.finish_order, name='finish_order'),
    url(r'^cancel_ordering/$', views.cancel_ordering, name='cancel_ordering'),

]