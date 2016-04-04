from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=200)
    op = models.CharField(max_length=200)
    activity = models.IntegerField()
    url = models.URLField(max_length=200)

    timestamp = models.DateTimeField(default=timezone.now)
    # latest_activity = models.DateTimeField(blank=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return unicode(self.title)

    def __repr__(self):
        return '<POST:{0}>'.format(self.title)


@python_2_unicode_compatible
class Subscriber(models.Model):
    email = models.EmailField(max_length=200)
    is_active = models.BooleanField(default=True)

    # user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.email)

    def __repr__(self):
        return '<SUBSCRIBER:{0}>'.format(self.email)
