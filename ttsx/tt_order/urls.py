from django.conf.urls import url
import views

urlpatterns=[
    url('^list/$',views.list),
    url('^handle/$',views.handle),
]
