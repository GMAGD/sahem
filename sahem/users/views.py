# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.datetime_safe import date, datetime
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.db.models import Q

from sahem.events.models import Event, Comment
from .models import User


# class UserDetailView(LoginRequiredMixin, DetailView):
#     model = User
#     # These next two lines tell the view to index lookups by username
#     slug_field = "username"
#     slug_url_kwarg = "username"


def detail(request, username):
    # Get the user
    user = User.objects.get(username=username)

    owner_events = []
    current_events = []
    upcoming_events = []
    finished_events = []
    comments = []

    # Get all owner created events
    try:
        owner_events = Event.objects.filter(owner=user)
    except:
        pass

    # Get all the current events
    try:
        current_events = Event.objects.filter(Q(staff__username=username) | Q(participant__username=username),
                                              Q(start__lte=date.today()) & Q(end__gt=date.today()))
    except:
        pass

    # Get all the upcomming events
    try:
        upcoming_events = Event.objects.filter(Q(staff__username=username) | Q(participant__username=username),
                                               Q(start__gt=date.today()))
    except:
        pass

    # Get all the finished events
    try:
        finished_events = Event.objects.filter(Q(staff__username=username) | Q(participant__username=username),
                                               Q(end__lt=date.today()))
    except:
        pass
    events_count = len(current_events) + len(upcoming_events)
    current_count = len(current_events)
    upcoming_count = len(upcoming_events)
    finished_count = len(finished_events)

    # Get all comments realted to the user fillter by latest adedd
    try:
        comments = Comment.objects.filter(user=user).order_by('created')
    except:
        pass

    print 'current events :' + str(current_events)
    print 'upcomming events :' + str(upcoming_events)
    print 'comments :' + str(comments)
    context = {
        'user': user,
        'owner_events': owner_events,
        'current_events': current_events,
        'upcoming_events': upcoming_events,
        'comments': comments,
        'events_count': events_count,
        'current_count': current_count,
        'upcoming_count': upcoming_count,
        'finished_count': finished_count

    }
    return render(request, 'users/user_detail.html', context)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
