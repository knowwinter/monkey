# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-11-12 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('das', '0023_auto_20181109_1436'),
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
            model_name='media',
            name='alt',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='media',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
    ]