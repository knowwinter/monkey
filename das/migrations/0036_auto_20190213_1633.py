# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-02-13 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('das', '0035_auto_20190212_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='menu_name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='menu_option',
            name='option_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='menu_option_template',
            name='option_name',
            field=models.CharField(max_length=100),
        ),
    ]
