# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-15 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('das', '0014_auto_20180511_1039'),
    ]

    operations = [
        # migrations.RenameField(
        #     model_name='comment',
        #     old_name='comment_autor',
        #     new_name='comment_author',
        # ),
        # migrations.RemoveField(
        #     model_name='article',
        #     name='article_mime_type',
        # ),
        # migrations.AddField(
        #     model_name='article',
        #     name='guid',
        #     field=models.URLField(blank=True, null=True),
        # ),
        migrations.AddField(
            model_name='comment',
            name='comment_status',
            field=models.CharField(choices=[('1', 'open'), ('2', 'close')], default='2', max_length=1),
        ),
    ]
