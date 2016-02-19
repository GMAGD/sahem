from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from geoposition.fields import GeopositionField

from sahem.users.models import User


# Create your models here.


# TODO create the Category class


class Event(models.Model):
    # Every event is realted to one owner
    owner = models.ForeignKey(User, related_name='event_owner')

    # Event staff
    staff = models.ManyToManyField(User, related_name='staffs', blank=True)

    # Event participant
    participant = models.ManyToManyField(User, related_name='participants', blank=True)

    name = models.CharField(max_length=170, null=False, blank=False)
    description = models.TextField()

    # Event date created
    created = models.DateTimeField(auto_now_add=True)

    # Event start and end date
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)

    position = GeopositionField()

    def get_staff_count(self):
        return self.staff.count()

    def get_participant_count(self):
        return self.participant.count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'id': self.id})
