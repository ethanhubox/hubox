from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add_merchant$', views.add_merchant, name='add_merchant'),
    url(r'^payment$', views.payment, name='payment'),

]
