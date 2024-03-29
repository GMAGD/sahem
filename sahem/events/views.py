# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datetime_safe import datetime
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

import json

from sahem.events.serializers import EventSerializer, UserSerializer, CategorySerializer, CommentSerializer
from sahem.users.models import User
from .forms import EventForm
from .models import Event, Category, Comment


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def list(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    events = Event.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        events = events.filter(category=category)

    return render(request, 'events/list.html', locals())


def detail(request, id, slug):
    event = get_object_or_404(Event, pk=id, slug=slug)

    if event.end.day < datetime.now().day:
        event.available = False

    return render(request, 'events/detail.html', locals())


@login_required
def create(request):
    print request.POST

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.slug = slugify(instance.name)

            instance.save()

            context = {
                'message': 'Event created',
                'flag': 'success',
            }

            # return render(request, 'events/create.html', context)
            return redirect('/#/events')

        else:
            context = {
                'message': 'Form is invalid',
                'flag': 'error',
                'form': form,
            }
            return render(request, 'events/create.html', context)

    else:
        form = EventForm()

    context = {
        'form': form,
    }

    return render(request, 'events/create.html', context)


@login_required
def delete(request, id):
    event = get_object_or_404(Event, pk=id)

    # check if the sender is the acctual owner of the event
    if request.user == event.owner:
        event.delete()
    else:
        raise Http404
    return redirect('events:list')


class EventUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EventForm
    template_name = 'events/update.html'
    # we already imported User in the view code above, remember?
    model = Event

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("events:list")


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@csrf_exempt
def event_list(request, id=None, slug=None, category_slug=None):
    if request.method == 'GET':

        if category_slug:
            events = Event.objects.filter(category__slug=category_slug)
        elif id and slug:
            events = Event.objects.filter(id=id, slug=slug)
        else:
            events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)

        else:
            return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def event_detail(request, pk):
    """
    Retrieve, update or delete a code event.
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':

        #  slugify the name before saving
        request.POST['slug'] = slugify(request.POST['name'])

        data = JSONParser().parse(request)
        serializer = EventSerializer(event, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        event.delete()
        return HttpResponse(status=204)


@csrf_exempt
def join_event(request, event_id, staff_id=None, participant_id=None):
    staff_ids = []
    participant_ids = []

    # get the acctual event from the database
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return HttpResponse(status=404)

    # get all staff ids
    for i in event.staff.all():
        staff_ids.append(i.id)

    # get all participants ids
    for i in event.participant.all():
        participant_ids.append(i.id)

    print '-------------------------------------'
    print "staff ids : " + str(staff_ids)
    print 'participant ids' + str(participant_ids)

    # if it's a staff request
    if staff_id:
        try:
            staff = User.objects.get(pk=staff_id)
            # convert the staff id to an integer
            staff_id = int(staff_id)
            if staff_id not in staff_ids and staff_id not in participant_ids and staff != event.owner:
                event.staff.add(staff)

        except User.DoesNotExist:
            return HttpResponse(status=404)

    # if it's a participant request
    elif participant_id:
        try:
            participant = User.objects.get(pk=participant_id)
            # convert the participant id to an integer
            participant_id = int(participant_id)

            if participant_id not in participant_ids and participant_id not in staff_ids and participant != event.owner:
                event.participant.add(participant)


        except User.DoesNotExist:
            return HttpResponse(status=404)

    serializer = EventSerializer(event)

    return JSONResponse(serializer.data)


@csrf_exempt
def leave_event(request, event_id, staff_id=None, participant_id=None):
    # get the event from the data base
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponse(status=404)

    # if the user was a staff a this event
    if staff_id:
        event.staff.remove(staff_id)
    # else if he is a participant at this event
    elif participant_id:
        event.participant.remove(participant_id)

    # get back the responce a serialized event data
    serializer = EventSerializer(event)
    return JSONResponse(serializer.data)


@csrf_exempt
def add_comment(request):

    data =  json.loads(request.body)

    print data['user_id']
    print data['comment']

    try:
        event = Event.objects.get(id=data['event_id'])
    except Event.DoesNotExist:
        return HttpResponse(status=404)

    try:
        user = User.objects.get(id=data['user_id'])
    except User.DoesNotExist:
        return HttpResponse(status=404)

    comment_obj = Comment.objects.create(user=user, content=data['comment'])
    comment_obj.save()

    event.comments.add(comment_obj)
    event.save()


    serializer = EventSerializer(event)

    return JSONResponse(serializer.data)
