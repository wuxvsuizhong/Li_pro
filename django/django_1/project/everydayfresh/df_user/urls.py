from django.conf.urls import url
import views

urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^register_handle/$',views.register_handle),
    url(r'^register_exist/$',views.register_exist),
    url(r'^login_handle/$',views.login_handle),
    url(r'^login/$',views.user_login),
    url(r'^info/$',views.show_user_info),
    url(r'^logout/$', views.user_logout),
    url(r'^user_center_order(\d*)/$',views.user_center_order),
    url(r'^user_center_site/$',views.user_center_site),
    url(r'^change_address/$',views.change_address),
]
