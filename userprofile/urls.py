from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^create_profile/$', views.create_profile, name='create_profile'),
    url(r'^subscribe_ajax/$', views.subscribe_ajax, name='subscribe_ajax'),
]
