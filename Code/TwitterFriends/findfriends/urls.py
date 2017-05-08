from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^$', views.get_whole_net, name='whole'),
    url(r'^netjson/$', views.netjson, name='netjson'),
    url(r'^netgdf/$', views.netgdf, name='netgdf'),
    url(r'^netnet/$', views.netgdf, name='netnet'),
    url(r'^netgml/$', views.netgml, name='netgml'),
]
