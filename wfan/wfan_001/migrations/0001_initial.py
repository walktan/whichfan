# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-06 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='twitBay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twit_user_id', models.DecimalField(decimal_places=0, max_digits=30)),
                ('twit', models.CharField(max_length=300)),
                ('twit_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='twitCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twit_user_id', models.DecimalField(decimal_places=0, max_digits=30)),
                ('twit', models.CharField(max_length=300)),
                ('twit_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='twitDra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twit_user_id', models.DecimalField(decimal_places=0, max_digits=30)),
                ('twit', models.CharField(max_length=300)),
                ('twit_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='twitGia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twit_user_id', models.DecimalField(decimal_places=0, max_digits=30)),
                ('twit', models.CharField(max_length=300)),
                ('twit_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='twitSwa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twit_user_id', models.DecimalField(decimal_places=0, max_digits=30)),
                ('twit', models.CharField(max_length=300)),
                ('twit_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='twitTig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twit_user_id', models.DecimalField(decimal_places=0, max_digits=30)),
                ('twit', models.CharField(max_length=300)),
                ('twit_at', models.DateTimeField()),
            ],
        ),
    ]
