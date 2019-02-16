# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.contrib import auth
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import *
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import os

from das.common import cache_sitemeta
from das.models import *
from das.forms import *
from django.conf import settings
import hashlib
import time

# from django.http import HttpResponse, HttpRequest
settings.SITEMETA = cache_sitemeta()

def index_view(req, pindex):
    context = {}
    if req.session.get('user'):
        context = {"user": req.session['user']}

    posts = Article.objects.filter(article_status="1", article_type='post').order_by('-pub_date')
    hot_posts = Article.objects.filter(article_type='post', article_status='1').order_by('-view_count')[:5]
    last_posts = posts[:5]
    tools = Menu.objects.get(menu_name='默认右侧边栏', menu_type='tool')
    context['tools'] = tools.menu.all()

    # for post in articles:
    #     post.content = post.content[:20]
    #     posts.append(post)
    nodes = Category.objects.get_queryset()
    paginator = Paginator(posts, 5)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))
    tags = Tag.objects.all()
    context['tags'] = tags
    context['pages'] = page
    context['nodes'] = nodes
    # print(settings.SITEMETA.head_background_img)
    context['sitemeta'] = settings.SITEMETA
    context['hot_posts'] = hot_posts
    context['last_posts'] = last_posts
    return render(req, 'index/index.html', context)

def post_show(req, id):
    context = {}
    tags = Tag.objects.all()
    context['tags'] = tags
    posts = Article.objects.filter(article_status="1", article_type='post').order_by('pub_date')
    post = posts.get(pk=id, article_type='post')
    post.view_count = post.view_count + 1
    post.comment_count = post.comment_set.filter(comment_status=1).count()
    post.like_count = post.likearticleship_set.count()
    post.save(update_fields=['view_count', "comment_count", 'like_count'])
    pre_post = posts.filter(pub_date__lt=post.pub_date).last()
    next_post = posts.filter(pub_date__gt=post.pub_date).first()
    post.content = post.content.replace("[!--more--]", "")
    comments = Comment.objects.filter(article=post).filter(comment_status="1").order_by("-comment_date")
    nodes = Category.objects.get_queryset()
    context['post'] = post
    context['pre_post'] = pre_post
    context['next_post'] = next_post
    context['nodes'] = nodes
    context['comments'] = comments
    context['sitemeta'] = settings.SITEMETA
    return render(req, 'index/post-show.html', context)


def post_preview(req, id):
    context = {}
    tags = Tag.objects.all()
    context['tags'] = tags
    posts = Article.objects.filter(article_status="1", article_type='post').order_by('pub_date')
    post = Article.objects.get(pk=id, article_status="2", article_type='post')

    post.comment_count = post.comment_set.filter(comment_status=1).count()
    post.like_count = post.likearticleship_set.count()
    post.save(update_fields=["comment_count", 'like_count'])
    pre_post = posts.filter(pub_date__lt=post.pub_date).last()
    next_post = posts.filter(pub_date__gt=post.pub_date).first()
    post.content = post.content.replace("[!--more--]", "")
    comments = Comment.objects.filter(article=post).filter(comment_status="1").order_by("-comment_date")
    nodes = Category.objects.get_queryset()
    context['post'] = post
    context['pre_post'] = pre_post
    context['next_post'] = next_post
    context['nodes'] = nodes
    context['comments'] = comments
    context['sitemeta'] = settings.SITEMETA
    return render(req, 'index/post-show.html', context)

def category_show(req, cate_id, pindex):
    context = {}
    category = None
    context['sitemeta'] = settings.SITEMETA
    tags = Tag.objects.all()
    context['tags'] = tags
    if cate_id == '0':
        posts = Article.objects.filter(category=None, article_type='post')
    else:
        category = Category.objects.get(pk=cate_id)
        try:
            posts = Article.objects.filter(category=category, article_type='post').order_by('-pub_date')
        except:
            posts = None
            nodes = Category.objects.get_queryset()
            context['nodes'] = nodes
            context['cate'] = category
            context['pages'] = posts
            return render(req, 'index/category-show.html', context)

    paginator = Paginator(posts, 10)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))

    nodes = Category.objects.get_queryset()

    context['nodes'] = nodes
    context['pages'] = page
    context['cate'] = category

    return render(req, 'index/category-show.html', context)

def tag_show(req, tag_id, pindex):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    tag = Tag.objects.get(pk=tag_id)
    tags = Tag.objects.all()
    context['tags'] = tags
    try:
        posts = Article.objects.filter(tag=tag, article_type='post').order_by('-pub_date')
    except:
        posts = None
        nodes = Category.objects.get_queryset()
        context['nodes'] = nodes
        context['tag'] = tag
        context['pages'] = posts
        return render(req, 'index/tag-show.html', context)
    paginator = Paginator(posts, 2)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))

    nodes = Category.objects.get_queryset()

    context['nodes'] = nodes
    context['pages'] = page
    context['tag'] = tag

    return render(req, 'index/tag-show.html', context)


def user_show(req, user_id, pindex):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    user = User.objects.get(pk=user_id)
    tags = Tag.objects.all()
    context['tags'] = tags
    try:
        posts = Article.objects.filter(pub_author=user, article_type='post').order_by('-pub_date')
    except:
        posts = None
        nodes = Category.objects.get_queryset()
        context['nodes'] = nodes
        context['user'] = user
        context['pages'] = posts
        return render(req, 'index/user-show.html', context)
    paginator = Paginator(posts, 2)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))

    nodes = Category.objects.get_queryset()

    context['nodes'] = nodes
    context['pages'] = page
    context['user'] = user

    return render(req, 'index/user-show.html', context)


def get_favicon(req):
    return redirect(settings.SITEMETA.favicon)


def page_show(req, url_slug):
    context = {}
    tags = Tag.objects.all()
    context['tags'] = tags
    post = Article.objects.get(url_slug=url_slug, article_type='page')
    post.view_count = post.view_count + 1
    if post.comment_status == '1':
        post.comment_count = post.comment_set.filter(comment_status=1).count()
        post.save(update_fields=['view_count', "comment_count"])
        comments = Comment.objects.filter(article=post).filter(comment_status="1").order_by("-comment_date")
        context['comments'] = comments
    else:
        post.save(update_fields=['view_count'])
    post.content = post.content.replace("[!--more--]", "")

    nodes = Category.objects.get_queryset()
    context['post'] = post
    context['nodes'] = nodes

    context['sitemeta'] = settings.SITEMETA
    return render(req, 'index/page-show.html', context)
