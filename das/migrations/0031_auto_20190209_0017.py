# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-02-09 00:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('das', '0030_auto_20181210_1723'),
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
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
