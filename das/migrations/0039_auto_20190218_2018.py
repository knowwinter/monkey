# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-02-18 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('das', '0038_auto_20190213_2350'),
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
            model_name='menu_option',
            name='option_template',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
