from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=200)
    post = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default=u'undefined')

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return '<POST:{0}>'.format(self.title)


@python_2_unicode_compatible
class Subscriber(models.Model):
    email = models.EmailField(max_length=200)
    is_active = models.BooleanField(default=True)

    # user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return '<SUBSCRIBER:{0}>'.format(self.email)
