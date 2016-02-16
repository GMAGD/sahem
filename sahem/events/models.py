from __future__ import unicode_literals

from django.db import models
from geoposition.fields import GeopositionField
from sahem.users.models import User


# Create your models here.
class Event(models.Model):
    # Every event is realted to one owner
    owner = models.ForeignKey(User, related_name='event_owner')

    # Event staff
    staff = models.ManyToManyField(User, related_name='staffs', blank=True)

    # Event participant
    participant = models.ManyToManyField(User, related_name='participants', blank=True)


    name = models.CharField(max_length=170, null=False, blank=False)
    # description = models.TextField()
    #
    # slug = models.SlugField(max_length=200, unique=True)
    #
    # # Event date created
    # created = models.DateTimeField(auto_now_add=True)
    #
    # # Event start and end date
    # start = models.DateTimeField(blank=False, null=False)
    # end = models.DateTimeField(blank=False, null=False)

    position = GeopositionField()

    def __str__(self):
        return self.name
