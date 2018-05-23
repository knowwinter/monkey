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

    posts = Article.objects.all().order_by('-pub_date')

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
    context['pages'] = page
    context['nodes'] = nodes
    return render(req, 'index/index.html', context)

def post_show(req, id):
    context = {}
    posts = Article.objects.all().order_by('pub_date')
    post = posts.get(pk=id)
    post.view_count = post.view_count + 1
    post.comment_count = post.comment_set.filter(comment_status=1).count()
    post.save(update_fields=['view_count',"comment_count"])
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
    return render(req, 'index/post-show.html', context)
