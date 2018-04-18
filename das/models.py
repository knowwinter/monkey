# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from uuslug import slugify
# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to='static/assets/avatars/', default="/static/assets/avatar/avatar.png")

class Category(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")
    description = models.CharField(max_length=80)
    article_count = models.IntegerField(default=0)
    url_slug = models.SlugField(editable=False)

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=30, null=False)
    content = models.TextField()
    url_slug = models.SlugField(editable=False)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    pub_author = models.ForeignKey(User)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)
    article_status_choice = (
        ('1', 'publish'),
        ('2', 'close'),
    )
    article_status = models.CharField(
        max_length=1,
        choices=article_status_choice,
        default='1',
    )
    comment_status_choice = (
        ('1', 'open'),
        ('2', 'close'),
    )
    comment_status = models.CharField(
        max_length=1,
        choices=comment_status_choice,
        default='1',
    )
    article_type = models.CharField(max_length=30, default='post')
    article_mime_type = models.CharField(max_length=30)
    category = models.ForeignKey(Category)



    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField(max_length=80)
    user_id = models.IntegerField(default=0)
    comment_autor = models.CharField(max_length=30)
    article = models.ForeignKey(Article)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")
    comment_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=10, null=False, unique=True)
    description = models.CharField(max_length=80)
    url_slug = models.SlugField(editable=False)
    members = models.ManyToManyField(
        Article,
        through='Tagship',
        through_fields=('tag', 'article'),
    )
    create_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Tagship(models.Model):
    article = models.ForeignKey(Article)
    tag = models.ForeignKey(Tag)

