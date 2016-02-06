from __future__ import unicode_literals
from django.db import models

# Create your models here.

class twitDra(models.Model):
    twit_user_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twitSwa(models.Model):
    twit_user_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twitGia(models.Model):
    twit_user_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twitTig(models.Model):
    twit_user_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twitCar(models.Model):
    twit_user_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twitBay(models.Model):
    twit_user_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()