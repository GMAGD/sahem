# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework import routers

from sahem.events import views

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
                  url(r'^$', TemplateView.as_view(template_name='base.html'), name="home"),
                  url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),
                  url(r'^privacy\-policy/$', TemplateView.as_view(template_name='pages/privacy_policy.html'),
                      name="privacy_policy"),

                  # Django Admin, use {% url 'admin:index' %}
                  url(settings.ADMIN_URL, include(admin.site.urls)),

                  # User management
                  url(r'^users/', include("sahem.users.urls", namespace="users")),
                  url(r'^accounts/', include('allauth.urls')),

                  # Your stuff: custom urls includes go here
                  url(r'^events/', include('sahem.events.urls', namespace='events')),

                  # Join event api
                  url(r'^api/events/join/event/(?P<event_id>\d+)/staff/(?P<staff_id>\d+)/$', views.join_event,
                      name='join_event_as_staff'),
                  url(r'^api/events/join/event/(?P<event_id>\d+)/participant/(?P<participant_id>\d+)/$',
                      views.join_event,
                      name='join_event_as_participant'),
                  # Api Endpoint
                  url(r'^api/events/(?P<id>\d+)/(?P<slug>\w+)/$', views.event_list, name='event_by_id_slug'),
                  url(r'^api/events/category/(?P<category_slug>\w+)/$', views.event_list, name='event_by_category'),
                  url(r'^api/', include(router.urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permission Denied")}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        url(r'^500/$', default_views.server_error),
    ]
