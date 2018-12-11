# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-10 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('das', '0027_auto_20181115_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('access_dashboard', '\u666e\u901a\u7ba1\u7406\u5458'),
                                ('access_all', '\u8d85\u7ea7\u7ba1\u7406\u5458')),
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='auth.Group')),
                ('description', models.CharField(max_length=100)),
            ],
            bases=('auth.group',),
        ),
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
    ]
