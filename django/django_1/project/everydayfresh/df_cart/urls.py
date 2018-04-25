from django.conf.urls import url
import views

urlpatterns = [
    url(r'^cart/$',views.show_cart),
    url(r'^cart/add_(\d+)_(\d+)/$',views.add_goods),
    url(r'^cart/add_(\d+)/$',views.addone),
    url(r'^cart/get_count/$',views.get_count),
    url(r'^cart/change_count_(\d+)_(\d+)/$',views.change_count),
    url(r'^cart/delete_goods_(\d+)/$',views.delete_goods),
]
