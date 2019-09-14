
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^search/', include('searchEngine.urls')),
    url(r'^$', views.home_page , name="home"),
]
urlpatterns += staticfiles_urlpatterns()
