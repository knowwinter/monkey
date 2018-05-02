# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render


# from django.http import HttpResponse, HttpRequest


def index_view(req):
    context = {}
    if req.session.get('user'):
        context = {"user": req.session['user']}
    return render(req, 'index/index.html', context)
