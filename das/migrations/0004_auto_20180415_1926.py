# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-15 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('das', '0003_auto_20180415_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='url_slug',
            field=models.SlugField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='url_slug',
            field=models.SlugField(default=0, editable=False),
            preserve_default=False,
        ),
    ]
