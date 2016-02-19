from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [

    # Category and Event list
    url(r'^$', views.list, name='list'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', views.list, name='event_list_by_category'),

    # Event detail
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.detail, name='detail'),

    # Event create update and delete
    url(r'^create/$', views.create, name='create'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^update/(?P<pk>\d+)/$', views.EventUpdateView.as_view(), name='update')
]
