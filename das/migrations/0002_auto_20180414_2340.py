# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-14 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('das', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.FileField(default='/static/assets/avatar/avatar.png', upload_to='static/assets/avatars/'),
        ),
    ]
