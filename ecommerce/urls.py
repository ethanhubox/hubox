from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^vendor/list$', views.vendor_list, name='vendor_list'),
    url(r'^vendor/(?P<pk>\d+)/$', views.vendor_detail, name='vendor_detail'),
    url(r'^course/list$', views.course_list, name='course_list'),
    url(r'^course/(?P<pk>\d+)/$', views.course_detail, name='course_detail'),
    url(r'^ordering/(?P<pk>\d+)/$', views.ordering_detail, name='ordering_detail'),
    url(r'^subscribe_ajax/$', views.subscribe_ajax, name='subscribe_ajax'),
    url(r'^create_user_profile/$', views.create_user_profile, name='create_user_profile'),
    url(r'^edit_user_profile/$', views.edit_user_profile, name='edit_user_profile'),
    url(r'^user_profile/$', views.user_profile, name='user_profile'),
    url(r'^catagory_detail/(?P<pk>\d+)/$', views.catagory_detail, name='catagory_detail'),
]
