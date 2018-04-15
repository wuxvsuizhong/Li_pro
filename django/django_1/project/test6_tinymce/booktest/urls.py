from django.conf.urls import url
import views

urlpatterns=[
    url(r'test_editor/$',views.TestHtml),
    url(r'content/$',views.HtmlEditorHandle),
    url(r'cache1/$',views.cache1),
    url(r'mysearch/$',views.mysearch),
    url(r'celeryTest/$',views.celeryTest),
]