# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
#from django.http import HttpResponse, HttpRequest

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

def index_view(req):
    context = {}
    if req.session.get('user'):
        context = {"user": req.session['user']}
    return render(req, 'index/index.html', context)