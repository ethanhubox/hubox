from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^member_terms/$', views.member_terms, name='member_terms'),
    url(r'^privacy_policy/$', views.privacy_policy, name='privacy_policy'),
]
