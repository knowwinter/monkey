# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
#from django.http import HttpResponse, HttpRequest

from django.contrib import auth
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from das.models import *

from forms import *

from django.core.paginator import *



def register_view(req):
    context = {}
    context['box'] = 'signup'
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']

            user = auth.authenticate(username=username, password=password, email=email)
            if user:
                context['user'] = user
                context['msg'] = "用户已经存在"
                return render(req, 'das/msg.html', context)
            user = User.objects.create_user(username, email, password, telephone=telephone)
            user.save()
            context['msg'] = '注册成功'
            context['view'] = 'login'
            context['jump'] = '登录'
            return render(req, 'das/msg.html', context)
        else:
            context['msg'] = '表单无效'
            return render(req, 'das/msg.html', context)

    return render(req, 'das/login.html', context)

def login_view(req):
    context = {}
    context['box'] = 'login'
    if req.session.get('user'):
        # print req.session.get('user')
        #context = {'isLogin': True, 'pswd': True, 'user': req.session.get('user')}
        context['user'] = req.session.get('user')
        context['msg'] = '用户已经登录'

        return render(req, 'das/msg.html', context)
    elif req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(req, user)
                # print req.session
                req.session['user'] = user
                return redirect('/das')
            else:
                context['msg'] = "用户名或密码错误"
                context['view'] = 'login'
                render(req, 'das/msg.html', context)
        else:
            context['msg'] = "表单错误"
            context['view'] = 'login'
            render(req, 'das/msg.html', context)
    return render(req, 'das/login.html', context)



def logout_view(req):
    auth.logout(req)
    return redirect('/')

@login_required(login_url='/login')
def index_view(req):
    return render(req, 'das/index.html')

@login_required(login_url='/login')
def category_view(req, pindex):
    context = {}
    if req.method == 'POST':
        form = CateForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            parent = form.cleaned_data['parent']
            description = form.cleaned_data['description']

            is_exist = Category.objects.filter(name=name)
            if is_exist:
                context['msg'] = "分类目录已经存在"
                return render(req, 'das/msg.html', context)
            cate = Category.objects.create(name=name, parent=parent, description=description)
            cate.save()
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    cates = Category.objects.all()
    paginator = Paginator(cates, 10)
    if pindex == '':
        pindex = '1'
    page = paginator.page(int(pindex))
    context['page'] = page
    return render(req, 'das/category.html', context)

@login_required(login_url='/login')
def tag_view(req):
    return render(req, 'das/tag.html')

@login_required(login_url='/login')
def post_view(req):
    return render(req, 'das/post.html')

@login_required(login_url='/login')
def page_view(req):
    return render(req, 'das/page.html')

@login_required(login_url='/login')
def media_view(req):
    return render(req, 'das/media.html')
