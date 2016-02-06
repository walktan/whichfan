from __future__ import unicode_literals
from django.db import models

# Create your models here.

class twitChu(models.Model):
    twit = models.CharField(max_length=300)


class twitYaku(models.Model):
    twit = models.CharField(max_length=300)