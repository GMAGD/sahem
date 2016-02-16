from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView

from .forms import EventForm
from .models import Event


def list(request):
    events = Event.objects.all()
    return render(request, 'events/list.html', locals())


def detail(request, id):
    event = get_object_or_404(Event, pk=id)
    return render(request, 'events/detail.html', locals())


def create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()

            context = {
                'message': 'Event created',
                'flag': 'success',
            }

            return render(request, 'events/create.html', context)

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


def delete(request, id):
    event = get_object_or_404(Event, pk=id)
    event.delete()
    return redirect('events:list')

class EventUpdateView(UpdateView):
    fields = ['name','description', 'start', 'end', 'position', ]
    template_name = 'events/update.html'
    # we already imported User in the view code above, remember?
    model = Event

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("events:list")


