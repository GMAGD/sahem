from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from geoposition.fields import GeopositionField

from sahem.users.models import User


# Comment model
class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comment_owner')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='category/%Y/%m/%d', blank=False)

    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('events:event_list_by_category', args=[self.slug])

    def admin_image(self):
        return '<img src="%s" height=50>' % self.image.url

    admin_image.short_description = 'icon'
    admin_image.allow_tags = True


class Event(models.Model):
    # The event category
    category = models.ForeignKey(Category)

    # Every event is realted to one owner
    owner = models.ForeignKey(User, related_name='event_owner')

    # Event staff
    staff = models.ManyToManyField(User, related_name='staffs', blank=True)

    # Event participant
    participant = models.ManyToManyField(User, related_name='participants', blank=True)

    name = models.CharField(max_length=200, db_index=True, null=False, blank=False)
    slug = models.SlugField(max_length=200, db_index=True, blank=True)
    description = models.TextField(blank=True)

    # Event comments
    comments = models.ManyToManyField(Comment)

    # If the actual date is > event.end availabe = False
    available = models.BooleanField(default=True)

    # Event date created
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Event start and end date
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)

    # Event geo postion latitude and position_1
    position = GeopositionField()

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def get_staff_count(self):
        return self.staff.count()

    get_staff_count.short_description = 'satff'
    get_staff_count.allow_tags = True

    def get_participant_count(self):
        return self.participant.count()

    get_participant_count.short_description = 'participants'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('events:detail', args=[self.id, self.slug])

    def admin_image(self):
        return '<img src="%s" height=50>' % self.category.image.url

    admin_image.short_description = 'category icon'
    admin_image.allow_tags = True

    def latitude(self):
        return self.position.latitude

    def longitude(self):
        return self.position.longitude
