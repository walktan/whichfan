from __future__ import unicode_literals
from django.db import models

class TeamMst(models.Model):
    team_name = models.CharField(max_length=128, primary_key=True)
    team_id = models.DecimalField(max_digits=8, decimal_places=0)
    search_word = models.CharField(max_length=128)

class TweetTable(models.Model):
    team_name = models.ForeignKey(TeamMst)
    twit_id = models.DecimalField(max_digits=30, decimal_places=0)
    twit = models.CharField(max_length=300)
    twit_at = models.DateTimeField()