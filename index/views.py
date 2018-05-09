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

    posts = Article.objects.all()

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
    post = Article.objects.get(pk=id)
    post.view_count = post.view_count + 1
    post.save()
    post.content = post.content.replace("[!--more--]", "")
    nodes = Category.objects.get_queryset()
    context['post'] = post
    context['nodes'] = nodes
    return render(req, 'index/post-show.html', context)
