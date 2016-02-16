from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # add views here
    url(r'^$', views.list, name='list'),
    url(r'^detail/(?P<id>\d+)/$', views.detail, name='detail'),
    url(r'^create/$', views.create, name='create'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^update/(?P<pk>\d+)/$', views.EventUpdateView.as_view(), name='update')
]
