from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datetime_safe import datetime
from django.utils.text import slugify
from django.views.generic import UpdateView

from .forms import EventForm
from .models import Event, Category


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
            return HttpResponse('<h1>Event Created</h1>')

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
    event.delete()
    return redirect('events:list')


class EventUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EventForm
    template_name = 'events/update.html'
    # we already imported User in the view code above, remember?
    model = Event

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("events:list")
