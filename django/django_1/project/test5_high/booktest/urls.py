from  django.conf.urls import url
import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^uploadpic/$',views.uploadPic),
    url(r'^uploadHandle$',views.uploadHandle),
    url(r'^herolist/(\d+)*/?$',views.herolist),
    url(r'^area/$',views.area),
    url(r'^area/(\d+)/$',views.area2),
    url(r'^city/(\d+)/$',views.city),
]
