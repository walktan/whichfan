from __future__ import unicode_literals
from django.db import models

# Create your models here.

class twitDra(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twitSwa(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twitGia(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twitTig(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twitCar(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twitBay(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()








class twiDra(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twiSwa(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twiGia(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twiTig(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twiCar(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

class twiBay(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()