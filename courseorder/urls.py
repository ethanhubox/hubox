from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^course_order_detail/(?P<pk>\d+)/$', views.course_order_detail, name='course_order_detail'),
    url(r'^course_check_out/$', views.course_check_out, name='course_check_out'),
    url(r'^create_order/$', views.create_order, name='create_order'),
    url(r'^voucher_check/$', views.voucher_check, name='voucher_check'),
    url(r'^cancel_course_order/$', views.cancel_course_order, name='cancel_course_order'),
    url(r'^finish_course_order/$', views.finish_course_order, name='finish_course_order'),
    url(r'^course_order_refund/$', views.course_order_refund, name='course_order_refund'),    
]
