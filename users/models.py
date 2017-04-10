# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(verbose_name='creation date', auto_now=True)
    done = models.BooleanField(default=False, verbose_name='Done')
    deleted = models.BooleanField(default=False, verbose_name='Deleted')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.creation_date)
