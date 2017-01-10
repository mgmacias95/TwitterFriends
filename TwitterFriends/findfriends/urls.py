from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^netjson/$', views.netjson, name='netjson'),
    url(r'^netgdf/$', views.netgdf, name='netgdf'),
]
