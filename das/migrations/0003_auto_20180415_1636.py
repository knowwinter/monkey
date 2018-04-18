# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-15 08:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('das', '0002_auto_20180414_2340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('url_slug', models.SlugField(editable=False)),
                ('view_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('last_modify', models.DateTimeField(auto_now=True)),
                ('article_status', models.CharField(choices=[('1', 'publish'), ('2', 'close')], default='1', max_length=1)),
                ('comment_status', models.CharField(choices=[('1', 'open'), ('2', 'close')], default='1', max_length=1)),
                ('article_type', models.CharField(default='post', max_length=30)),
                ('article_mime_type', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('parent', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=80)),
                ('article_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=80)),
                ('user_id', models.IntegerField(default=0)),
                ('comment_autor', models.CharField(max_length=30)),
                ('parent', models.IntegerField(default=0)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='das.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
                ('description', models.CharField(max_length=80)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tagship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='das.Article')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='das.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='members',
            field=models.ManyToManyField(through='das.Tagship', to='das.Article'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='das.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='pub_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]