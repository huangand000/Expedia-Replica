# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-21 01:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='travel',
            name='start_date',
            field=models.DateField(),
        ),
    ]