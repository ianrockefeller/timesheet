# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-21 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itimetracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttask',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
