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
from das.models import *
from das.forms import *
from django.conf import settings
import hashlib
import time

# from django.http import HttpResponse, HttpRequest


def index_view(req, pindex):
    context = {}
    if req.session.get('user'):
        context = {"user": req.session['user']}

    posts = Article.objects.filter(article_status="1").order_by('-pub_date')

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
    sitemeta = get_sitemeta(req)
    context['tags'] = tags
    context['pages'] = page
    context['nodes'] = nodes
    context['sitemeta'] = sitemeta
    return render(req, 'index/index.html', context)

def post_show(req, id):
    context = {}
    tags = Tag.objects.all()
    context['tags'] = tags
    posts = Article.objects.filter(article_status="1").order_by('pub_date')
    post = posts.get(pk=id)
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
    sitemeta = get_sitemeta(req)
    context['sitemeta'] = sitemeta
    return render(req, 'index/post-show.html', context)


def post_preview(req, id):
    context = {}
    tags = Tag.objects.all()
    context['tags'] = tags
    posts = Article.objects.filter(article_status="1").order_by('pub_date')
    post = Article.objects.get(pk=id, article_status="2")

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
    sitemeta = get_sitemeta(req)
    context['sitemeta'] = sitemeta
    return render(req, 'index/post-show.html', context)

def category_show(req, cate_id, pindex):
    context = {}
    category = None
    tags = Tag.objects.all()
    context['tags'] = tags
    if cate_id == '0':
        posts = Article.objects.filter(category=None)
    else:
        category = Category.objects.get(pk=cate_id)
        try:
            posts = Article.objects.filter(category=category).order_by('-pub_date')
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
    sitemeta = get_sitemeta(req)
    context['sitemeta'] = sitemeta
    return render(req, 'index/category-show.html', context)

def tag_show(req, tag_id, pindex):
    context = {}
    tag = Tag.objects.get(pk=tag_id)
    tags = Tag.objects.all()
    context['tags'] = tags
    try:
        posts = Article.objects.filter(tag=tag).order_by('-pub_date')
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
    sitemeta = get_sitemeta(req)
    context['sitemeta'] = sitemeta
    return render(req, 'index/tag-show.html', context)

def get_sitemeta(req):
    sitemeta = Sitemeta.objects.all()[0]
    return sitemeta

def get_favicon(req):
    sitemeta = get_sitemeta(req)
    return redirect(sitemeta.favicon)