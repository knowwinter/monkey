# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-02-23 21:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('das', '0042_auto_20190222_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='position',
        ),
        migrations.AddField(
            model_name='menu_position',
            name='menu',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='menu_position', to='das.Menu'),
        ),
    ]
