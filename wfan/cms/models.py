from __future__ import unicode_literals
from django.db import models


#ドラゴンズ関連ツイート
class twitDra(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

#スワローズ関連ツイート
class twitSwa(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

#ジャイアンツ関連ツイート
class twitGia(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

#タイガース関連ツイート
class twitTig(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

#カープ関連ツイート
class twitCar(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()

#ベイスターズ関連ツイート
class twitBay(models.Model):
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()