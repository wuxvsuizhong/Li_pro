from django.conf.urls import url
import views
urlpatterns=[
    url(r'^$',views.index),
    url(r'^index/$',views.show_index),
    url(r'^list_(\d+)_(\d+)_(\d+)/$',views.show_list),
    url(r'^detail_(\d+)/$',views.show_detail),
]