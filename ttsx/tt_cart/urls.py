from django.conf.urls import url
import views
urlpatterns=[
    url('^add/$',views.add),
    url('^$',views.cart),
    url('^delcart/$',views.delcart),
    url('^set/$',views.set),
    url('^count/$',views.count),
]
