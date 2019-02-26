# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import *
from django.db import models
from mptt.models import MPTTModel
from uuslug import slugify


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    telephone = models.CharField(max_length=11, null=False, unique=True)
    email = models.EmailField(unique=True, null=False)
    avatar = models.FileField(upload_to='static/assets/avatars/', default="/static/assets/avatars/avatar.png")
    like_comment = models.ManyToManyField(
        'Comment',
        related_name="comment_like_user",
        through='Likecommentship',
        through_fields=('user', 'comment'),

    )
    like_article = models.ManyToManyField(
        'Article',
        related_name="article_like_user",
        through='Likearticleship',
        through_fields=('user', 'article'),
    )


class Category(MPTTModel):
    name = models.CharField(max_length=30, null=False, unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")
    description = models.CharField(max_length=80)
    article_count = models.IntegerField(default=0)
    url_slug = models.SlugField(editable=False)

    def __unicode__(self):
        return unicode(self.name)


class Article(models.Model):
    title = models.CharField(max_length=30, null=False)
    content = models.TextField(blank=True, null=True)
    url_slug = models.SlugField(editable=False)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)

    comment_count = models.IntegerField(default=0)
    pub_author = models.ForeignKey(User, related_name='author')
    # like_user = models.ManyToManyField(
    #     User,
    #     # through='Likearticleship',
    #     # through_fields=('likeuser', 'likearticle'),
    # )
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
        default='2',
    )
    article_type = models.CharField(max_length=30, default='post')
    # article_mime_type = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    # parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")
    guid = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.title)


class Comment(models.Model):
    comment = models.TextField(max_length=80)
    user = models.ForeignKey(User, blank=True, null=True, related_name="commenter")
    comment_author = models.CharField(max_length=30)
    article = models.ForeignKey(Article)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_author_ip = models.GenericIPAddressField(blank=True, null=True)
    comment_author_email = models.EmailField(blank=True, null=True)
    comment_modify_date = models.DateTimeField(auto_now=True)
    comment_status_choice = (
        ('1', 'open'),
        ('2', 'close'),
    )
    comment_status = models.CharField(
        max_length=1,
        choices=comment_status_choice,
        default='2',
    )


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
        return unicode(self.name)


class Tagship(models.Model):
    article = models.ForeignKey(Article)
    tag = models.ForeignKey(Tag)


class Likearticleship(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)



class Likecommentship(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)

class Sitemeta(models.Model):
    site_name = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=100, null=True)
    keywords = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=100, null=False)
    title = models.CharField(max_length=100, null=True)
    subtitle = models.CharField(max_length=100, null=True)
    announcement = models.CharField(max_length=50, null=True)
    favicon = models.CharField(max_length=255, null=True)
    head_background_img = models.CharField(max_length=100, default='static/assets/img/1.jpg', null=False)
    author_img = models.CharField(max_length=255, null=True)
    head_code = models.CharField(max_length=2000, null=True)
    foot_code = models.CharField(max_length=2000, null=True)
    is_weibo = models.CharField(max_length=1, default='0')
    wb_uid = models.CharField(max_length=15, null=True)
    is_wechat = models.CharField(max_length=1, default='0')
    wechat_qrcode = models.CharField(max_length=255, null=True)
    is_qqgroup = models.CharField(max_length=1, default='0')
    qqgroup_url = models.CharField(max_length=500, null=True)
    is_twitter = models.CharField(max_length=1, default='0')
    twitter_id = models.CharField(max_length=50, null=True)

class Media(models.Model):
    file_name = models.CharField(max_length=100, null=False)
    o_file_name = models.CharField(max_length=100, null=False)
    file_local_path = models.CharField(max_length=200, null=False, unique=True)
    file_url = models.CharField(max_length=255, null=False, unique=True)
    file_type = models.CharField(max_length=10, null=False)
    file_author = models.ForeignKey(User, related_name='file_author')
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, null=True)
    alt = models.CharField(max_length=50, null=True)
    members = models.ManyToManyField(
        Article,
        through='Mediaship',
        through_fields=('media', 'article'),
    )
    def save(self, *args, **kwargs):
        super(Media, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.file_name)

class Mediaship(models.Model):
    media = models.ForeignKey(Media)
    article = models.ForeignKey(Article)
    ship_date = models.DateTimeField(auto_now_add=True)


class AccessControl(models.Model):
    """
    自定义权限控制
    """

    class Meta:
        permissions = (
            ('access_dashboard', u'普通管理员'),
            ('access_all', u'超级管理员'),
            ('access_member', u'普通会员'),
        )



class Menu(models.Model):
    menu_name = models.CharField(max_length=100, null=False, unique=True)
    menu_type = models.CharField(max_length=20, null=False)


class Menu_position(models.Model):
    position = models.CharField(max_length=30, null=False)
    menu = models.ForeignKey(Menu, related_name='menu_position', null=True, default=None)

class Menu_option_template(models.Model):
    option_name = models.CharField(max_length=100, null=False)
    option_value = models.CharField(max_length=2000, null=True)


class Menu_option(models.Model):
    option_name = models.CharField(max_length=100, null=False)
    option_title = models.CharField(max_length=30, null=True)
    original_title = models.CharField(max_length=30, null=True)
    option_value = models.CharField(max_length=2000, null=True)
    option_icon = models.CharField(max_length=30, null=True)
    menu = models.ForeignKey(Menu, related_name='menu')
    user_menu = models.ForeignKey(Menu, related_name='user_menu', null=True, default=None)
    option_level = models.IntegerField(default=1)
    option_template = models.CharField(max_length=2000, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")
