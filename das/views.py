# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
from forms import *
from django.conf import settings
import hashlib
import time


# from django.http import HttpResponse, HttpRequest


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
        # context = {'isLogin': True, 'pswd': True, 'user': req.session.get('user')}
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
                return render(req, 'das/msg.html', context)
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
            parent_id = form.cleaned_data['parent']
            if parent_id == 0:
                parent = None
            else:
                parent = Category.objects.get(pk=parent_id)
            # parent = Category.objects.get(pk=parent_id)
            description = form.cleaned_data['description']
            url_slug = form.cleaned_data['url_slug']

            is_exist = Category.objects.filter(name=name)
            if is_exist:
                context['msg'] = "分类目录已经存在"
                return render(req, 'das/msg.html', context)
            cate = Category.objects.create(name=name, parent=parent, description=description, url_slug=url_slug)
            cate.save()
            context['msg'] = "目录创建成功"
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    nodes = Category.objects.get_queryset()
    # nodes = cates.tree.all()

    paginator = Paginator(nodes, 5)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))
    context['pages'] = page
    context['nodes'] = nodes
    return render(req, 'das/category.html', context)


@login_required(login_url='/login')
def category_del(req, pindex, cate_id):
    context = {}
    cate = Category.objects.get(pk=cate_id)
    if not cate:
        context['msg'] = '目录不存在'
        return render(req, 'das/msg.html', context)

    cate.delete()
    context['msg'] = '删除成功'

    return redirect('/das/category/' + pindex, context)


@login_required(login_url='/login')
def category_modify(req, cate_id):
    context = {}
    cate = Category.objects.get(pk=cate_id)
    if not cate:
        context['msg'] = '目录不存在'
        return render(req, 'das/msg.html', context)

    if req.method == 'POST':
        form = CateForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            parent_id = form.cleaned_data['parent']
            if parent_id == 0:
                parent = None
            else:
                parent = Category.objects.get(pk=parent_id)
            # parent = Category.objects.get(pk=parent_id)
            description = form.cleaned_data['description']
            url_slug = form.cleaned_data['url_slug']

            is_exist = Category.objects.filter(name=name).filter(~Q(pk=cate_id))
            if is_exist:
                context['msg'] = "分类目录已经存在"
                return render(req, 'das/msg.html', context)
            cate.name = name
            cate.parent = parent
            cate.decription = description
            cate.url_slug = url_slug
            cate.save()
            context['msg'] = '修改成功'
            return redirect('/das/category/', context)
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    nodes = Category.objects.get_queryset()
    context['cate'] = cate
    context['nodes'] = nodes
    return render(req, 'das/cate-modify.html', context)


@login_required(login_url='/login')
def tag_view(req, pindex):
    context = {}
    if req.method == 'POST':
        form = TagForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            is_exist = Tag.objects.filter(name=name)
            if is_exist:
                context['msg'] = "标签已经存在"
                return render(req, 'das/msg.html', context)
            tag = Tag.objects.create(name=name, description=description)
            tag.save()
            context['msg'] = "标签创建成功"
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    tags = Tag.objects.all()
    paginator = Paginator(tags, 5)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))
    context['pages'] = page
    return render(req, 'das/tag.html', context)


@login_required(login_url='/login')
def tag_del(req, pindex, tag_id):
    context = {}
    tag = Tag.objects.get(pk=tag_id)
    if not tag:
        context['msg'] = '标签不存在'
        return render(req, 'das/msg.html', context)

    tag.delete()
    context['msg'] = '删除成功'

    return redirect('/das/tag/' + pindex, context)


@login_required(login_url='/login')
def tag_modify(req, tag_id):
    context = {}
    tag = Tag.objects.get(pk=tag_id)
    if not tag:
        context['msg'] = '标签不存在'
        return render(req, 'das/msg.html', context)

    if req.method == 'POST':
        form = TagForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            is_exist = Tag.objects.filter(name=name).filter(~Q(pk=tag_id))
            if is_exist:
                context['msg'] = "标签已经存在"
                return render(req, 'das/msg.html', context)
            tag.name = name
            tag.description = description
            tag.save()
            context['msg'] = '修改成功'
            return redirect('/das/tag/', context)
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    context['tag'] = tag

    return render(req, 'das/tag-modify.html', context)


@login_required(login_url='/login')
def post_new_view(req):
    context = {}
    if req.method == "POST":
        form = PostForm(req.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            pub_author = User.objects.get(pk=form.cleaned_data['pub_author'])
            article_status = form.cleaned_data['article_status']
            comment_status = form.cleaned_data['comment_status']
            article_type = form.cleaned_data['article_type']
            article_mime_type = form.cleaned_data['article_mime_type']
            category_id = form.cleaned_data['category']

            parent = None

            if category_id == 0:
                category = None
            else:
                category = Category.objects.get(pk=category_id)
            tags = form.cleaned_data['tags']
            post = Article.objects.create(title=title, content=content, pub_author=pub_author,
                                          article_status=article_status, comment_status=comment_status,
                                          article_type=article_type, article_mime_type=article_mime_type,
                                          category=category, parent=parent)
            post.save()
            post.guid = '/p/' + post.pk
            post.save()
            if tags != None:
                for tag_id in tags:
                    tag = Tag.objects.get(pk=tag_id)
                    tagship = Tagship.objects.create(post, tag)
                    tagship.save()
            if article_status == '2':
                context['msg'] = '文章草稿保存成功'
            else:
                context['msg'] = "文章发表成功"
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    nodes = Category.objects.get_queryset()
    context['nodes'] = nodes
    allTags = Tag.objects.all()
    context['tags'] = allTags
    return render(req, 'das/post-new.html', context)


@login_required(login_url='/login')
def post_modify(req, article_id):
    context = {}
    post = Article.objects.get(pk=article_id)
    if not post:
        context['msg'] = '文章不存在'
        return render(req, 'das/msg.html', context)
    if req.method == "POST":
        form = PostForm(req.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            article_status = form.cleaned_data['article_status']
            comment_status = form.cleaned_data['comment_status']
            category_id = form.cleaned_data['category']
            if category_id == 0:
                category = None
            else:
                category = Category.objects.get(pk=category_id)
            tags = form.cleaned_data['tags']

            post.title = title
            post.content = content
            post.article_status = article_status
            post.comment_status = comment_status
            post.category = category
            post.save()
            post_tags = Tagship.objects.get(article=post)
            for post_tag in post_tags:
                post_tag.delete()
            if tags != None:
                for tag_id in tags:
                    tag = Tag.objects.get(pk=tag_id)
                    tagship = Tagship.objects.create(post, tag)
                    tagship.save()
            if article_status == '2':
                context['msg'] = '文章草稿保存成功'
            else:
                context['msg'] = "文章发表成功"
            return redirect('/das/post/', context)
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    nodes = Category.objects.get_queryset()
    context['nodes'] = nodes
    allTags = Tag.objects.all()
    context['tags'] = allTags
    context['post'] = post
    return render(req, 'das/post-modify.html', context)


@login_required(login_url='/login')
def post_del(req, pindex, article_id):
    context = {}
    post = Article.objects.get(pk=article_id)
    if not post:
        context['msg'] = '文章不存在'
        return render(req, 'das/msg.html', context)
    post.delete()
    context['msg'] = '删除成功'

    return redirect('/das/post/' + pindex, context)


@login_required(login_url='/login')
def post_view(req, pindex):
    context = {}
    articles = Article.objects.all()
    paginator = Paginator(articles, 10)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))
    context['pages'] = page
    context['post'] = articles
    return render(req, 'das/post.html', context)


@login_required(login_url='/login')
def page_view(req, pindex):
    context = {}
    articles = Article.objects.get(article_type='page')
    paginator = Paginator(articles, 10)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))
    context['pages'] = page
    context['post'] = articles
    return render(req, 'das/page.html', context)


@login_required(login_url='/login')
def page_new_view(req):
    context = {}
    if req.method == "POST":
        form = PostForm(req.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            pub_author = User.objects.get(pk=form.cleaned_data['pub_author'])
            article_status = form.cleaned_data['article_status']
            comment_status = form.cleaned_data['comment_status']
            article_type = form.cleaned_data['article_type']
            article_mime_type = form.cleaned_data['article_mime_type']

            parent = None

            category = None
            # tags = form.cleaned_data['tags']

            guid = '/page/' + title
            post = Article.objects.create(title=title, content=content, pub_author=pub_author,
                                          article_status=article_status, comment_status=comment_status,
                                          article_type=article_type, article_mime_type=article_mime_type,
                                          category=category, parent=parent, guid=guid)
            post.save()


            if article_status == '2':
                context['msg'] = '文章草稿保存成功'
            else:
                context['msg'] = "文章发表成功"
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    # nodes = Category.objects.get_queryset()
    # context['nodes'] = nodes
    # allTags = Tag.objects.all()
    # context['tags'] = allTags
    return render(req, 'das/page-new.html', context)


@login_required(login_url='/login')
def page_modify(req, article_id):
    context = {}
    post = Article.objects.get(pk=article_id, article_type='page')
    if not post:
        context['msg'] = '页面不存在'
        return render(req, 'das/msg.html', context)
    if req.method == "POST":
        form = PostForm(req.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            article_status = form.cleaned_data['article_status']
            comment_status = form.cleaned_data['comment_status']

            post.title = title
            post.content = content
            post.article_status = article_status
            post.comment_status = comment_status

            post.save()
            if article_status == '2':
                context['msg'] = '文章草稿保存成功'
            else:
                context['msg'] = "文章发表成功"
            return redirect('/das/page/', context)
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    context['post'] = post
    return render(req, 'das/page-modify.html', context)


@login_required(login_url='/login')
def page_del(req, pindex, article_id):
    context = {}
    post = Article.objects.get(pk=article_id, article_type='page')
    if not post:
        context['msg'] = '页面不存在'
        return render(req, 'das/msg.html', context)
    post.delete()
    context['msg'] = '删除成功'

    return redirect('/das/page/' + pindex, context)


# @login_required(login_url='/login')
# def media_view(req, pindex):
#     context = {}
#     articles = Article.objects.get(article_type='attachment')
#     paginator = Paginator(articles, 10)
#     if pindex == '':
#         pindex = '1'
#     try:
#         page = paginator.page(int(pindex))
#     except:
#         pindex = int(pindex) - 1
#         page = paginator.page(int(pindex))
#     context['pages'] = page
#     context['post'] = articles
#
#     return render(req, 'das/attachment.html', context)
#
#
# @login_required(login_url='/login')
# def media_new_page(req):
#     context = {}
#     if req.method == "POST":
#         form = PostForm(req.POST)
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             content = form.cleaned_data['content']
#             pub_author = User.objects.get(pk=form.cleaned_data['pub_author'])
#             article_status = form.cleaned_data['article_status']
#             comment_status = form.cleaned_data['comment_status']
#             article_type = form.cleaned_data['article_type']
#             article_mime_type = form.cleaned_data['article_mime_type']
#             category = None
#             parent_id = form.cleaned_data['parent']
#             if parent_id == 0:
#                 parent = None
#             else:
#                 parent = Article.objects.get(pk=parent_id)
#             # tags = form.cleaned_data['tags']
#             post = Article.objects.create(title=title, content=content, pub_author=pub_author,
#                                           article_status=article_status, comment_status=comment_status,
#                                           article_type=article_type, article_mime_type=article_mime_type,
#                                           category=category, parent=parent)
#             post.save()
#
#             if article_status == '2':
#                 context['msg'] = '文章草稿保存成功'
#             else:
#                 context['msg'] = "文章发表成功"
#         else:
#             context['msg'] = "表单错误"
#             return render(req, 'das/msg.html', context)
#     # nodes = Category.objects.get_queryset()
#     # context['nodes'] = nodes
#     # allTags = Tag.objects.all()
#     # context['tags'] = allTags
#     return render(req, 'das/attachment-new.html', context)

# @login_required(login_url='/login')
def upload(req):
    ret = {"error":True,"path":"http:\/\/www.mydomain.com\/myimage.jpg"}
    if req.method == "POST":
        ret = handle_upload_file(req.FILES['file'], str(req.FILES['file']), req.get_host())

    return HttpResponse(json.dumps(ret), content_type="application/json")  # 此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中

# @login_required(login_url='/login')
def handle_upload_file(file, filename, host):
    m = hashlib.md5()
    m.update(bytes(str(time.time()).encode('utf8')))
    filename = m.hexdigest() + os.path.splitext(filename)[1]
    uploadpath = time.strftime('%Y%m%d', time.localtime(time.time()))
    path = os.path.join(settings.UPLOAD_ROOT, uploadpath)  # 上传文件的保存路径，可以自己指定任意的路径
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + '/' + filename, 'wb+')as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    except:
        ret = {"error": True, "path": ""}
        return ret
    url = 'http://' + host + settings.MEDIA_ROOT + uploadpath + "/" + filename
    ret = {"error": 'false', "url": url}
    return ret
