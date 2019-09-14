from django.conf.urls import url
from . import views

app_name = 'searchEngine'

urlpatterns = [
    #url(r'^$', views.homepage, name="search"),
    url(r'^login$', views.fun1),
    url(r'^otp$', views.fun2),
    #url(r'^(?P<slug>[\w\W]+)$', views.reviewPage, name="reviewdisplay"),
]
