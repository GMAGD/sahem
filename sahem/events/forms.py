from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'category', 'description', 'start', 'end', 'position', ]
