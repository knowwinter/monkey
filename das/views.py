# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import json
import os
import time
from itertools import count

from django.conf import settings
from django.contrib import auth
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import *
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from das.common import cache_sitemeta
from das.models import *
from forms import *
from common import *
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.forms import formset_factory
from datetime import datetime, timedelta
from django.db.models import Avg, Max, Min, Sum
# from django.http import HttpResponse, HttpRequest
settings.SITEMETA = cache_sitemeta()

def register_view(req):
    context = {}
    context['box'] = 'signup'
    context['sitemeta'] = settings.SITEMETA
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
            perm = Permission.objects.get(codename='access_member')
            user.user_permissions.add(perm)
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
    context['sitemeta'] = settings.SITEMETA
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


@login_required(login_url='/login.html')
def index_view(req):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['version'] = settings.VIERSION
    context['active'] = 'das_index'
    dt_s = datetime.now()
    dt_e = (dt_s - timedelta(7))
    if req.user.is_superuser or req.user.has_perm('access_dashboard'):
        post_count = Article.objects.filter(article_type='post', article_status='1').count()
        last_week_pub_post_count = Article.objects.filter(article_type='post', article_status='1',
                                                          last_modify__range=(dt_e, dt_s)).count()
        if post_count and post_count - last_week_pub_post_count != 0:
            post_grow = round((last_week_pub_post_count * 100) / (post_count - last_week_pub_post_count), 2)
        elif post_count - last_week_pub_post_count == 0:
            post_grow = last_week_pub_post_count * 100
        else:
            post_grow = 0
        user_count = User.objects.all().count()
        last_week_new_user_count = User.objects.filter(date_joined__range=(dt_e, dt_s)).count()
        if user_count and user_count - last_week_new_user_count != 0:
            user_grow = round((last_week_new_user_count * 100) / (user_count - last_week_new_user_count), 2)
        elif user_count - last_week_new_user_count == 0:
            user_grow = last_week_new_user_count * 100
        else:
            user_grow = 0
        comment_count = Comment.objects.all().count()
        last_week_new_comment_count = Comment.objects.filter(comment_date__range=(dt_e, dt_s)).count()
        if comment_count and comment_count - last_week_new_comment_count != 0:
            comment_grow = round((last_week_new_comment_count * 100) / (comment_count - last_week_new_comment_count), 2)
        elif comment_count - last_week_new_comment_count == 0:
            comment_grow = last_week_new_comment_count * 100
        else:
            comment_grow = 0
        post_views = Article.objects.filter(article_type='post', article_status='1').aggregate(Sum('view_count'))[
            'view_count__sum']
        tag_count = Tag.objects.all().count()
        # category_count = count(Category.objects.get_queryset())
        category_count = 10
        last_week_new_users = User.objects.filter(date_joined__range=(dt_e, dt_s)).order_by('date_joined')
        last_comments = Comment.objects.all().order_by('-comment_date')[:5]
        context['post_count'] = post_count
        context['post_grow'] = post_grow
        context['last_week_pub_post_count'] = last_week_pub_post_count
        context['user_count'] = user_count
        context['user_grow'] = user_grow
        context['last_week_new_user_count'] = last_week_new_user_count
        context['comment_count'] = comment_count
        context['comment_grow'] = comment_grow
        context['last_week_new_comment_count'] = last_week_new_comment_count
        context['tag_count'] = tag_count
        context['category_count'] = category_count
        context['post_views'] = post_views
        context['last_week_new_users'] = last_week_new_users
        context['last_comments'] = last_comments

    my_post_count = Article.objects.filter(article_type='post', article_status='1', pub_author=req.user).count()
    my_last_week_pub_post_count = Article.objects.filter(article_type='post', article_status='1', pub_author=req.user,
                                                         last_modify__range=(dt_e, dt_s)).count()
    if my_post_count and my_post_count - my_last_week_pub_post_count != 0:
        my_post_grow = round((my_last_week_pub_post_count * 100) / (my_post_count - my_last_week_pub_post_count), 2)
    elif my_post_count - my_last_week_pub_post_count == 0:
        my_post_grow = my_last_week_pub_post_count * 100
    else:
        my_post_grow = 0
    my_comment_count = Comment.objects.filter(user=req.user).count()
    my_last_week_new_comment_count = Comment.objects.filter(user=req.user, comment_date__range=(dt_e, dt_s)).count()
    if my_comment_count and my_comment_count - my_last_week_new_comment_count != 0:
        my_comment_grow = round(
            (my_last_week_new_comment_count * 100) / (my_comment_count - my_last_week_new_comment_count), 2)
    elif my_comment_count - my_last_week_new_comment_count == 0:
        my_comment_grow = my_last_week_new_comment_count * 100
    else:
        my_comment_grow = 0
    my_post_views = \
    Article.objects.filter(pub_author=req.user, article_type='post', article_status='1').aggregate(Sum('view_count'))[
        'view_count__sum']
    if not my_post_views:
        my_post_views = 0
    my_post_likes = \
    Article.objects.filter(pub_author=req.user, article_type='post', article_status='1').aggregate(Sum('like_count'))[
        'like_count__sum']
    if not my_post_likes:
        my_post_likes = 0
    my_comment_like_count = Likecommentship.objects.filter(comment__in=Comment.objects.filter(user=req.user)).count()
    hot_posts = Article.objects.filter(article_type='post', article_status='1').order_by('-view_count')[:5]
    my_comments = Comment.objects.filter(Q(user=req.user) | Q(parent__comment__in=req.user.commenter.all())).order_by(
        '-comment_date')[:5]
    my_last_posts = Article.objects.filter(article_status='1', article_type='post', pub_author=req.user).order_by(
        '-last_modify')[0:5]

    context['my_post_count'] = my_post_count
    context['my_last_week_pub_post_count'] = my_last_week_pub_post_count
    context['my_post_grow'] = my_post_grow
    context['my_comment_count'] = my_comment_count
    context['my_last_week_new_comment_count'] = my_last_week_new_comment_count
    context['my_comment_grow'] = my_comment_grow
    context['my_post_views'] = my_post_views
    context['my_post_likes'] = my_post_likes
    context['hot_posts'] = hot_posts
    context['my_comments'] = my_comments
    context['my_comment_like_count'] = my_comment_like_count
    context['my_last_posts'] = my_last_posts


    return render(req, 'das/index.html', context)


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def category_view(req, pindex):
    context = {}
    context['active'] = 'category'
    context['sitemeta'] = settings.SITEMETA
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


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def category_del(req, pindex, cate_id):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'category'
    cate = Category.objects.get(pk=cate_id)
    if not cate:
        context['msg'] = '目录不存在'
        return render(req, 'das/msg.html', context)

    cate.delete()
    context['msg'] = '删除成功'

    return redirect('/das/category/' + pindex, context)


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def category_modify(req, cate_id):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'category'
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


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def tag_view(req, pindex):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'tag'
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


@login_required(login_url='/login.html')
def json_get_tags(req):
    tags = Tag.objects.all()
    tag_list = []
    for tag in tags:
        t = {'id': tag.pk, 'label': tag.name, 'value': tag.name}
        tag_list.append(t)
    return HttpResponse(json.dumps(tag_list), content_type="application/json")


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def tag_del(req, pindex, tag_id):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'tag'
    tag = Tag.objects.get(pk=tag_id)
    if not tag:
        context['msg'] = '标签不存在'
        return render(req, 'das/msg.html', context)

    tag.delete()
    context['msg'] = '删除成功'

    return redirect('/das/tag/' + pindex, context)


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def tag_modify(req, tag_id):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'tag'
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


@login_required(login_url='/login.html')
def post_new_view(req):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'post_new'
    if req.method == "POST":
        form = PostForm(req.POST)
        if form.is_valid():
            postIsExist = None
            title = form.cleaned_data['title']
            try:
                postIsExist = Article.objects.get(title=title)
            except:
                pass
            if postIsExist:
                context['msg'] = '文章标题重名，请更换标题'
                return render(req, 'das/msg.html', context)

            content = form.cleaned_data['content']
            pub_author = User.objects.get(pk=form.cleaned_data['pub_author'])
            article_status = form.cleaned_data['article_status']
            if form.cleaned_data['comment_status'] == '':
                comment_status = '2'
            else:
                comment_status = form.cleaned_data['comment_status']
            article_type = form.cleaned_data['article_type']
            # article_mime_type = form.cleaned_data['article_mime_type']
            category_id = form.cleaned_data['category']

            # parent = None

            if category_id == 0:
                category = None
            else:
                category = Category.objects.get(pk=category_id)
            tags = form.cleaned_data['tags']
            post = Article.objects.create(title=title, content=content, pub_author=pub_author,
                                          article_status=article_status, comment_status=comment_status,
                                          article_type=article_type,
                                          category=category)
            post.guid = '/p/' + str(post.pk)
            post.save()
            # post = Article.objects.get(title=title)
            # post.guid = '/p/' + post.pk
            # post.save()
            if tags != '':
                tags = tags.split(',')
                for tagName in tags:
                    try:
                        tag = Tag.objects.get(name=tagName)
                    except:
                        tag = Tag.objects.create(name=tagName, description=tagName)
                    tagship = Tagship.objects.create(article=post, tag=tag)
                    tagship.save()

            pattern = 'img src="(.*?)"'
            imgtmp = parseContent(post.content, pattern)
            if imgtmp:
               for file_url in imgtmp:
                   try:
                        media = Media.objects.get(file_url=file_url)
                        mediaship = Mediaship.objects.create(media=media, article=post)
                        mediaship.save()
                   except:
                       pass

            pattern_2 = 'a href="(.*?)"'
            attachmenttmp = parseContent(post.content, pattern_2)
            if attachmenttmp:
                for file_url in attachmenttmp:
                    try:
                        media = Media.objects.get(file_url=file_url)
                        mediaship = Mediaship.objects.create(media=media, article=post)
                        mediaship.save()
                    except:
                        pass

            if article_status == '2':
                context['msg'] = '文章草稿保存成功'
            else:
                context['msg'] = "文章发表成功"
            return redirect("/", context)
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    nodes = Category.objects.get_queryset()
    context['nodes'] = nodes
    allTags = Tag.objects.all()
    context['tags'] = allTags
    return render(req, 'das/post-new.html', context)


@login_required(login_url='/login.html')
def post_modify(req, article_id):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'post_all'
    user = req.session.get('user')
    if user.is_superuser or user.has_perm('das.access_dashboard'):
        post = Article.objects.get(pk=article_id)
    else:
        post = Article.objects.get(pk=article_id, pub_author=user)
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
            post.tag_set.clear()

            post.media_set.clear()
            post.save()

            # post_tags = Tagship.objects.get(article=post)
            # for post_tag in post_tags:
            #     post_tag.delete()
            if tags != '':
                tags = tags.split(',')
                for tagName in tags:
                    try:
                        tag = Tag.objects.get(name=tagName)
                    except:
                        tag = Tag.objects.create(name=tagName, description=tagName)
                    tagship = Tagship.objects.create(article=post, tag=tag)
                    tagship.save()

            pattern = 'img src="(.*?)"'
            imgtmp = parseContent(post.content, pattern)
            if imgtmp:
                for file_url in imgtmp:
                    try:
                        media = Media.objects.get(file_url=file_url)
                        mediaship = Mediaship.objects.create(media=media, article=post)
                        mediaship.save()
                    except:
                        pass

            pattern_2 = 'a href="(.*?)"'
            attachmenttmp = parseContent(post.content, pattern_2)
            if attachmenttmp:
                for file_url in attachmenttmp:
                    try:
                        media = Media.objects.get(file_url=file_url)
                        mediaship = Mediaship.objects.create(media=media, article=post)
                        mediaship.save()
                    except:
                        pass

            if article_status == '2':
                context['msg'] = '文章草稿保存成功'
            else:
                context['msg'] = "文章发表成功"
            return redirect('/das/post/list/1', context)
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    nodes = Category.objects.get_queryset()
    context['nodes'] = nodes
    allTags = Tag.objects.all()
    context['tags'] = allTags
    context['post'] = post
    return render(req, 'das/post-modify.html', context)


@login_required(login_url='/login.html')
def post_del(req, pindex, article_id, article_status):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'post_all'
    user = req.session.get('user')
    if user.is_superuser or user.has_perm('das.access_dashboard'):
        post = Article.objects.get(pk=article_id)
    else:
        post = Article.objects.get(pk=article_id, pub_author=user)
    if not post:
        context['msg'] = '文章不存在'
        return render(req, 'das/msg.html', context)
    post.delete()
    context['msg'] = '删除成功'
    context['article_status'] = article_status
    return redirect('/das/post/list/' + pindex + '/' + article_status, context)


@login_required(login_url='/login.html')
def post_revoke(req, pindex, article_id, article_status):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'post_all'
    user = req.session.get('user')
    if user.is_superuser or user.has_perm('das.access_dashboard'):
        post = Article.objects.get(pk=article_id)
    else:
        post = Article.objects.get(pk=article_id, pub_author=user)
    if not post:
        context['msg'] = '文章不存在'
        return render(req, 'das/msg.html', context)
    post.article_status = "2"
    post.save()
    context['msg'] = '文章撤回成功'
    context['article_status'] = article_status
    return redirect('/das/post/list/' + pindex + '/' + article_status, context)


@login_required(login_url='/login.html')
def post_view(req, pindex, article_status):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'post_all'
    if article_status == "":
        article_status = '0'
    if req.method == 'POST':
        form = ArticleStatusForm(req.POST)
        if form.is_valid():
            article_status = form.cleaned_data['article_status']
    user = req.session.get('user')
    if user.is_superuser or user.has_perm('das.access_dashboard'):
        if article_status == '0':
            articles = Article.objects.filter(article_type='post').order_by("-pub_date")
        else:
            articles = Article.objects.filter(article_status=article_status, article_type='post').order_by("-pub_date")
    else:
        if article_status == '0':
            articles = Article.objects.filter(pub_author=user, article_type='post').order_by("-pub_date")
        else:
            articles = Article.objects.filter(pub_author=user, article_status=article_status,
                                              article_type='post').order_by("-pub_date")
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
    context['article_status'] = article_status
    return render(req, 'das/posts-list.html', context)


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def page_view(req, pindex):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'page_all'
    articles = Article.objects.filter(article_type='page').order_by("-pub_date")
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
    return render(req, 'das/pages-list.html', context)


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def page_new_view(req):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'page_new'
    if req.method == "POST":
        form = PostForm(req.POST)
        if form.is_valid():
            postIsExist = None
            title = form.cleaned_data['title']
            try:
                postIsExist = Article.objects.get(title=title)
            except:
                pass
            if postIsExist:
                context['msg'] = '页面标题重名，请更换标题'
                return render(req, 'das/msg.html', context)

            content = form.cleaned_data['content']
            pub_author = User.objects.get(pk=form.cleaned_data['pub_author'])
            article_status = 1
            if form.cleaned_data['comment_status'] == '':
                comment_status = '2'
            else:
                comment_status = form.cleaned_data['comment_status']
            article_type = 'page'
            # article_mime_type = form.cleaned_data['article_mime_type']

            # parent = None


            post = Article.objects.create(title=title, content=content, pub_author=pub_author,
                                          article_status=article_status, comment_status=comment_status,
                                          article_type=article_type)
            post.guid = '/page/' + str(post.pk)
            post.save()
            # post = Article.objects.get(title=title)
            # post.guid = '/p/' + post.pk
            # post.save()

            pattern = 'img src="(.*?)"'
            imgtmp = parseContent(post.content, pattern)
            if imgtmp:
                for file_url in imgtmp:
                    try:
                        media = Media.objects.get(file_url=file_url)
                        mediaship = Mediaship.objects.create(media=media, article=post)
                        mediaship.save()
                    except:
                        pass

            pattern_2 = 'a href="(.*?)"'
            attachmenttmp = parseContent(post.content, pattern_2)
            if attachmenttmp:
                for file_url in attachmenttmp:
                    try:
                        media = Media.objects.get(file_url=file_url)
                        mediaship = Mediaship.objects.create(media=media, article=post)
                        mediaship.save()
                    except:
                        pass

            context['msg'] = "页面创建成功"
            return redirect("/das/page/list/1", context)
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)

    return render(req, 'das/page-new.html', context)


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def page_modify(req, article_id):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'page_all'
    post = Article.objects.get(pk=article_id, article_type='page')
    if not post:
        context['msg'] = '页面不存在'
        return render(req, 'das/msg.html', context)
    if req.method == "POST":
        form = PostForm(req.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            article_status = 1
            comment_status = form.cleaned_data['comment_status']

            post.title = title
            post.content = content
            post.article_status = article_status
            post.comment_status = comment_status
            post.media_set.clear()
            post.save()

            # post_tags = Tagship.objects.get(article=post)
            # for post_tag in post_tags:
            #     post_tag.delete()

            pattern = 'img src="(.*?)"'
            imgtmp = parseContent(post.content, pattern)
            if imgtmp:
                for file_url in imgtmp:
                    try:
                        media = Media.objects.get(file_url=file_url)
                        mediaship = Mediaship.objects.create(media=media, article=post)
                        mediaship.save()
                    except:
                        pass

            pattern_2 = 'a href="(.*?)"'
            attachmenttmp = parseContent(post.content, pattern_2)
            if attachmenttmp:
                for file_url in attachmenttmp:
                    try:
                        media = Media.objects.get(file_url=file_url)
                        mediaship = Mediaship.objects.create(media=media, article=post)
                        mediaship.save()
                    except:
                        pass

            context['msg'] = "页面修改成功"
            return redirect('/das/page/list/1', context)
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    context['post'] = post
    return render(req, 'das/page-modify.html', context)


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def page_del(req, pindex, article_id):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'page_all'
    post = Article.objects.get(pk=article_id, article_type='page')
    if not post:
        context['msg'] = '页面不存在'
        return render(req, 'das/msg.html', context)
    post.delete()
    context['msg'] = '删除成功'
    return redirect('/das/page/list/' + pindex, context)


# @login_required(login_url='/login.html')
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
# @login_required(login_url='/login.html')
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

# @login_required(login_url='/login.html')
def upload(req, user_id):
    ret = {"error": True, "path": ""}
    if req.method == "POST":
        uploadtype = None
        if 'uploadtype' in req.POST.keys():
            uploadtype = req.POST['uploadtype']
        ret = handle_upload_file(req.FILES['file'], str(req.FILES['file']), req.scheme, req.get_host(), uploadtype, user_id, str(req.FILES['file']), str(req.FILES['file']))

    return HttpResponse(json.dumps(ret), content_type="application/json")  # 此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中


# @login_required(login_url='/login.html')
def handle_upload_file(file, filename, schema, host, uploadtype, user_id, description, alt):
    m = hashlib.md5()
    m.update(bytes(str(time.time()).encode('utf8')))

    o_filename = filename

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
    url = schema + '://' + host + settings.MEDIA_ROOT + uploadpath + "/" + filename
    file_type = os.path.splitext(filename)[1][1:]
    file_local_path = path + '/' + filename
    file_author = User.objects.get(pk=user_id)
    media = Media.objects.create(file_name=filename, o_file_name=o_filename, file_local_path=file_local_path, file_url=url, file_type=file_type, file_author=file_author, description=description, alt=alt)
    try:
        media.save()
    except:
        ret = {"error": True, "path": ""}
        return ret
    ret = {"error": 'false', "url": url, "uploadtype": uploadtype, "o_filename": o_filename, "description": media.description, "alt": media.alt, "id":  media.pk}
    return ret


def comment(req):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    if req.method == "POST":
        # print req.POST
        form = CommentForm(req.POST)
        if form.is_valid():
            timeformat = "%Y年%m月%d日 %H:%M".encode('utf8')
            comment = form.cleaned_data['comment']
            user_id = form.cleaned_data['user']
            comment_status = "2"
            if not user_id:
                user = None
            else:
                user = User.objects.get(pk=user_id)
                if user.is_superuser == 1 or user.has_perm('access_dashboard'):
                    comment_status = "1"

            comment_author = form.cleaned_data['comment_author']
            comment_author_email = form.cleaned_data['comment_author_email']
            article_id = form.cleaned_data['article']
            article = Article.objects.get(pk=article_id)
            parent_id = form.cleaned_data['parent']
            if not parent_id:
                parent = None
            else:
                parent = Comment.objects.get(pk=parent_id)
                parent_comment_date = parent.comment_date.strftime(timeformat)
            comment_author_ip = form.cleaned_data['comment_author_ip']
            comm = Comment.objects.create(comment=comment, user=user, comment_author=comment_author,
                                          comment_author_email=comment_author_email, article=article, parent=parent,
                                          comment_author_ip=comment_author_ip, comment_status=comment_status)
            comm.save()
            if comm.comment_status == '1':
                article.comment_count = article.comment_count + 1
                article.save(update_fields=['comment_count'])

            comment_time = comm.comment_date.strftime(timeformat)

            if user and parent:
                jsondata = {"id": comm.pk, "comment": comm.comment, "comment_author": comm.comment_author,
                            "comment_date": comment_time, "avatar": str(user.avatar),
                            "parent_author": parent.comment_author, "parent_comment_date": parent_comment_date,
                            "parent_comment": parent.comment, "comment_status": comment_status,
                            "comment_count": article.comment_count, "comment_author_ip": comm.comment_author_ip,
                            "article_guid": article.guid, "article_title": article.title,
                            "comment_author_email": comm.comment_author_email, "article_id": article.pk}
            elif parent:
                jsondata = {"id": comm.pk, "comment": comm.comment, "comment_author": comm.comment_author,
                            "comment_date": comment_time, "avatar": "/static/assets/avatars/avatar.png",
                            "parent_author": parent.comment_author, "parent_comment_date": parent_comment_date,
                            "parent_comment": parent.comment, "comment_status": comment_status,
                            "comment_count": article.comment_count, "comment_author_ip": comm.comment_author_ip,
                            "article_guid": article.guid, "article_title": article.title,
                            "comment_author_email": comm.comment_author_email, "article_id": article.pk}
            elif user:
                jsondata = {"id": comm.pk, "comment": comm.comment, "comment_author": comm.comment_author,
                            "comment_date": comment_time, "avatar": str(user.avatar), "comment_status": comment_status,
                            "comment_count": article.comment_count, "comment_author_ip": comm.comment_author_ip,
                            "article_guid": article.guid, "article_title": article.title,
                            "comment_author_email": comm.comment_author_email, "article_id": article.pk}
            else:
                jsondata = {"id": comm.pk, "comment": comm.comment, "comment_author": comm.comment_author,
                            "comment_date": comment_time, "avatar": "/static/assets/avatars/avatar.png",
                            "comment_status": comment_status, "comment_count": article.comment_count,
                            "comment_author_ip": comm.comment_author_ip, "article_guid": article.guid,
                            "article_title": article.title, "comment_author_email": comm.comment_author_email,
                            "article_id": article.pk}

            return HttpResponse(json.dumps(jsondata), content_type="application/json")
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    else:
        context['msg'] = '非法操作'
        return render(req, 'das/msg.html', context)


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url="/login")
def comment_show(req, pindex, comment_status):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'comment_show'
    if comment_status == "":
        comment_status = '0'
    if req.method == "POST":
        form = CommentStatusForm(req.POST)
        if form.is_valid():
            comment_status = form.cleaned_data['comment_status']

    user = req.session.get('user')
    if user.is_superuser or user.has_perm('das.access_dashboard'):
        if comment_status == '0':
            comments = Comment.objects.all().order_by('-comment_date')
        else:
            comments = Comment.objects.filter(comment_status=comment_status).order_by('-comment_date')
    else:
        if comment_status == '0':
            comments = Comment.objects.filter(user=user).order_by('-comment_date')
        else:
            comments = Comment.objects.filter(user=user, comment_status=comment_status).order_by('-comment_date')
    paginator = Paginator(comments, 10)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))
    context['pages'] = page
    context['comments'] = comments
    context['comment_status'] = comment_status
    return render(req, 'das/comment-show.html', context)


@login_required(login_url="/login")
def my_comment(req, pindex, comment_status):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'my_comment'
    if comment_status == "":
        comment_status = '0'
    if req.method == "POST":
        form = CommentStatusForm(req.POST)
        if form.is_valid():
            comment_status = form.cleaned_data['comment_status']

    user = req.session.get('user')
    if comment_status == '0':
        comments = Comment.objects.filter(user=user).order_by('-comment_date')
    else:
        comments = Comment.objects.filter(user=user, comment_status=comment_status).order_by('-comment_date')
    paginator = Paginator(comments, 10)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))
    context['pages'] = page
    context['comments'] = comments
    context['comment_status'] = comment_status
    return render(req, 'das/my-comment.html', context)


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url="/login")
def comment_audit(req, comment_id, oper):
    context = {}
    # context['sitemeta'] = settings.SITEMETA
    context['active'] = 'comment_show'
    comment = Comment.objects.get(pk=comment_id)
    if comment:
        if oper == "reject":
            # ret = comment_del(req, comment_id)
            comment.comment_status = "2"
            comment.save()

            context['msg'] = "评论驳回成功"
            context['result'] = "success"

        elif oper == "accept":
            comment.comment_status = "1"
            comment.save()
            article = comment.article
            article.comment_count = article.comment_count + 1
            article.save()
            context['msg'] = "评论审核通过"
            context['result'] = "success"
    else:
        context['msg'] = "评论不存在"
        context['result'] = "failure"
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required(login_url="/login")
def comment_del(req, comment_id):
    context = {}
    # context['sitemeta'] = settings.SITEMETA
    context['active'] = 'comment_show'
    user = req.session.get('user')
    if user.is_superuser or user.has_perm('das.access_dashboard'):
        comment = Comment.objects.get(pk=comment_id)
    else:
        comment = Comment.objects.get(user=user, pk=comment_id)
    if comment:

        article = comment.article

        comment.delete()
        article.comment_count = article.comment_set.filter(comment_status=1).count()
        article.save()
        context['result'] = "success"
        context['msg'] = "评论删除成功"
        context['comment_count'] = article.comment_count
    else:
        context['result'] = "failure"
        context['msg'] = "评论不存在"
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required(login_url="/login")
def like_article(req, article_id, user_id):
    context = {}
    # context['sitemeta'] = settings.SITEMETA
    article = Article.objects.get(pk=article_id)
    user = User.objects.get(pk=user_id)
    try:
        likearticleship = Likearticleship.objects.filter(user=user, article=article)

        if likearticleship:
            likearticleship[0].delete()
        else:
            likearticleship = Likearticleship.objects.create(user=user, article=article)
            likearticleship.save()
        context['result'] = 'success'
    except:
        context['result'] = 'failure'
    finally:
        return HttpResponse(json.dumps(context), content_type="application/json")


@login_required(login_url="/login")
def like_comment(req, comment_id, user_id):
    context = {}
    # context['sitemeta'] = settings.SITEMETA
    comment = Comment.objects.get(pk=comment_id)
    user = User.objects.get(pk=user_id)
    try:
        likecommentship = Likecommentship.objects.filter(user=user, comment=comment)

        if likecommentship:
            likecommentship[0].delete()
        else:
            likecommentship = Likecommentship.objects.create(user=user, comment=comment)
            likecommentship.save()
        context['result'] = 'success'
    except:
        context['result'] = 'failure'
    finally:
        return HttpResponse(json.dumps(context), content_type="application/json")


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url="/login")
def set_site(req):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'set_site'
    site_meta = None
    try:
        site_meta = Sitemeta.objects.all()[0]
    except:
        site_meta = None
    if req.method == 'POST':
        form = SiteMetaForm(req.POST)
        if form.is_valid():
            site_name = form.cleaned_data['site_name']
            description = form.cleaned_data['description']
            keywords = form.cleaned_data['keywords']
            author = form.cleaned_data['author']
            title = form.cleaned_data['title']
            subtitle = form.cleaned_data['subtitle']
            announcement = form.cleaned_data['announcement']
            favicon = form.cleaned_data['favicon']
            head_background_img = form.cleaned_data['head_background_img']
            author_img = form.cleaned_data['author_img']
            head_code = form.cleaned_data['head_code']
            foot_code = form.cleaned_data['foot_code']
            is_weibo = form.cleaned_data['is_weibo']
            if not is_weibo:
                is_weibo = 0
            wb_uid = form.cleaned_data['wb_uid']
            is_wechat = form.cleaned_data['is_wechat']
            if not is_wechat:
                is_wechat = 0
            wechat_qrcode = form.cleaned_data['wechat_qrcode']
            is_qqgroup = form.cleaned_data['is_qqgroup']
            if not is_qqgroup:
                is_qqgroup = 0
            qqgroup_url = form.cleaned_data['qqgroup_url']
            is_twitter = form.cleaned_data['is_twitter']
            if not is_twitter:
                is_twitter = 0
            twitter_id = form.cleaned_data['twitter_id']
            if not site_meta:
                site_meta = Sitemeta.objects.create(site_name=site_name, description=description, keywords=keywords,
                                                    author=author, title=title, subtitle=subtitle,
                                                    announcement=announcement,
                                                    favicon=favicon, head_background_img=head_background_img,
                                                    author_img=author_img, head_code=head_code, foot_code=foot_code,
                                                    is_weibo=is_weibo, wb_uid=wb_uid, is_wechat=is_wechat,
                                                    wechat_qrcode=wechat_qrcode, is_qqgroup=is_qqgroup,
                                                    qqgroup_url=qqgroup_url, is_twitter=is_twitter, twitter_id=twitter_id)
            else:
                site_meta.site_name = site_name
                site_meta.description = description
                site_meta.keywords = keywords
                site_meta.author = author
                site_meta.title = title
                site_meta.subtitle = subtitle
                site_meta.announcement = announcement
                site_meta.favicon = favicon
                site_meta.head_background_img = head_background_img
                site_meta.author_img = author_img
                site_meta.head_code = head_code
                site_meta.foot_code = foot_code
                site_meta.is_weibo = is_weibo
                site_meta.wb_uid = wb_uid
                site_meta.is_wechat = is_wechat
                site_meta.wechat_qrcode = wechat_qrcode
                site_meta.is_qqgroup = is_qqgroup
                site_meta.qqgroup_url = qqgroup_url
                site_meta.is_twitter = is_twitter
                site_meta.twitter_id = twitter_id
            site_meta.save()
            context['sitemeta'] = cache_sitemeta(change=True)
            settings.SITEMETA = site_meta
            context['site_meta'] = site_meta
            return render(req, 'das/site_edit.html', context)
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    context['site_meta'] = site_meta
    return render(req, 'das/site_edit.html', context)

@login_required(login_url="/login")
def upload_page(req, pindex):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    user = req.session.get('user')
    if user.is_superuser or user.has_perm('das.access_dashboard'):
        medias = Media.objects.all().order_by("-upload_date")
    else:
        medias = Media.objects.filter(file_author=user).order_by("-upload_date")
    paginator = Paginator(medias, 10)
    active = 'active'
    if pindex == '':
        pindex = '1'
        active = None
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))
    context['pages'] = page

    context['media'] = medias
    context['active'] = active
    return render(req, 'das/dropzone.html', context)

@login_required(login_url="/login")
def media_view(req, pindex):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'media_all'
    user = req.session.get('user')
    if user.is_superuser or user.has_perm('das.access_dashboard'):
        medias = Media.objects.all().order_by("-upload_date")
    else:
        medias = Media.objects.filter(file_author=user).order_by("-upload_date")
    paginator = Paginator(medias, 10)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))
    context['pages'] = page

    context['media'] = medias
    return render(req, 'das/media-show.html', context)


@login_required(login_url="/login")
def media_modify(req, id):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'media_all'
    user = req.session.get('user')
    if user.is_superuser or user.has_perm('das.access_dashboard'):
        media = Media.objects.get(pk=id)
    else:
        media = Media.objects.get(pk=id, file_author=user)
    if not media:
        context['msg'] = "媒体不存在"
        return render(req, 'das/msg.html', context)
    if req.method == 'POST':
        form = MediaForm(req.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            alt = form.cleaned_data['alt']
            o_file_name = form.cleaned_data['o_file_name']
            media.o_file_name = o_file_name
            media.description = description
            media.alt = alt
            try:
                media.save()
                context['msg'] = '修改成功'
                return redirect('/das/media/list/1', context)
            except:
                context['msg'] = '失败，请重试'
                return render(req, 'das/msg.html', context)
        else:
            context['msg'] = "表单错误"
            return render(req, 'das/msg.html', context)
    context['media'] = media
    return render(req, 'das/media-modify.html', context)

@login_required(login_url="/login")
def media_del(req, id):
    context = {}
    # context['sitemeta'] = settings.SITEMETA
    context['active'] = 'media_all'
    user = req.session.get('user')
    if user.is_superuser or user.has_perm('das.access_dashboard'):
        try:
            media = Media.objects.get(pk=id)
        except:
            context['msg'] = "媒体不存在"
            context['result'] = 'failure'
            return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        try:
            media = Media.objects.get(pk=id, file_author=user)
        except:
            context['msg'] = "媒体不存在"
            context['result'] = 'failure'
            return HttpResponse(json.dumps(context), content_type="application/json")

    try:
        os.remove(media.file_local_path)
        media.delete()
        context['msg'] = '媒体删除成功'
        context['result'] = 'success'
        return HttpResponse(json.dumps(context), content_type="application/json")
    except:
        context['msg'] = "媒体删除失败，请重试"
        context['result'] = 'failure'
        return HttpResponse(json.dumps(context), content_type="application/json")

@login_required(login_url="/login")
def media_del_by_o_name(req, o_name):
    context = {}
    # context['sitemeta'] = settings.SITEMETA
    user = req.session.get('user')
    if user.is_superuser or user.has_perm('das.access_dashboard'):
        try:
            media = Media.objects.filter(o_file_name=o_name).order_by("-upload_date")[0]
        except:
            context['msg'] = "媒体不存在"
            context['result'] = 'failure'
            return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        try:
            media = Media.objects.filter(o_file_name=o_name, file_author=user).order_by("-upload_date")[0]
        except:
            context['msg'] = "媒体不存在"
            context['result'] = 'failure'
            return HttpResponse(json.dumps(context), content_type="application/json")
    try:
        os.remove(media.file_local_path)
        media.delete()
        context['msg'] = '媒体删除成功'
        context['result'] = 'success'
        return HttpResponse(json.dumps(context), content_type="application/json")
    except:
        context['msg'] = "媒体删除失败，请重试"
        context['result'] = 'failure'
        return HttpResponse(json.dumps(context), content_type="application/json")


@login_required(login_url="/login")
def media_new_view(req):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'media_new'
    return render(req, 'das/media-add.html', context)


# def group_view(req):
#     context = {}
#     context['sitemeta'] = settings.SITEMETA
#     context['active'] = 'group_mgr'
#     groups = None
#     try:
#         groups = Group.objects.all()
#     except:
#         groups = None
#     finally:
#         context['groups'] = groups
#         return render(req, 'das/groups-list.html', context)
#
#
# def group_add_view(req):
#     context = {}
#     context['sitemeta'] = settings.SITEMETA
#     context['active'] = 'group_mgr'
#     if req.method == 'POST':
#         form = GroupForm(req.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             perm = form.cleaned_data['perm']
#             members = form.cleaned_data['members']
#             try:
#                 group = Group.objects.get(name=name)
#                 context['msg'] = "用户组已经存在"
#                 return render(req, 'das/msg.html', context)
#             except:
#                 group = Group.objects.create(name=name)
#                 group.save()
#                 permission = Permission.objects.get(codename=perm)
#                 group.permissions.add(permission)
#                 if members != '':
#                     members = members.split(',')
#                     for username in members:
#                         user = User.objects.get(username=username)
#                         group.user_set.add(user)
#                 context['msg'] = '用户组创建成功'
#                 return render(req, 'das/groups-list', context)
#         else:
#             context['msg'] = "表单错误"
#             return render(req, 'das/msg.html', context)
#     user = User.objects.all()
#     context['user'] = user
#     return render(req, 'das/group-add.html', context)
#
#
# def group_modify_view(req, group_id):
#     context = {}
#     context['sitemeta'] = settings.SITEMETA
#     context['active'] = 'group_mgr'
#     group = None
#     try:
#         group = Group.objects.get(pk=group_id)
#     except:
#         context['msg'] = '用户组不存在'
#         return render(req, 'das/msg.html', context)
#     if req.method == 'POST':
#         form = GroupForm(req.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             perm = form.cleaned_data['perm']
#             members = form.cleaned_data['members']
#             group.name = name
#             group.user_set.clear()
#             group.permissions.clear()
#             group.save()
#             permission = Permission.objects.get(codename=perm)
#             group.permissions.add(permission)
#             if members != '':
#                 members = members.split(',')
#                 for username in members:
#                     user = User.objects.get(username=username)
#                     group.user_set.add(user)
#             context['msg'] = '用户组修改成功'
#             return render(req, 'das/groups-list', context)
#         else:
#             context['msg'] = "表单错误"
#             return render(req, 'das/msg.html', context)
#     user = User.objects.all()
#     context['group'] = group
#     context['user'] = user
#     return render(req, 'das/group-modify.html', context)
#
#
# def group_del_view(req, group_id):
#     context = {}
#     context['sitemeta'] = settings.SITEMETA
#     context['active'] = 'group_mgr'
#     group = None
#     try:
#         group = Group.objects.get(pk=group_id)
#         group.user_set.clear()
#         group.permissions.clear()
#         group.delete()
#         context['msg'] = '用户组删除成功'
#     except:
#         context['msg'] = '用户组不存在'
#         return render(req, 'das/msg.html', context)
#     return render(req, 'das/groups-list.html', context)

@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def user_view(req, pindex, status):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'user_mgr'

    if status == "":
        status = '2'
    if req.method == 'POST':
        form = UserStatusForm(req.POST)
        if form.is_valid():
            status = form.cleaned_data['user_status']
    if status == '2':
        users = User.objects.all().order_by('-date_joined')
    else:
        status = int(status)
        users = User.objects.filter(is_active=status).order_by('-date_joined')

    paginator = Paginator(users, 10)
    if pindex == '':
        pindex = '1'
    try:
        page = paginator.page(int(pindex))
    except:
        pindex = int(pindex) - 1
        page = paginator.page(int(pindex))
    context['pages'] = page
    context['users'] = users
    context['user_status'] = str(status)
    return render(req, 'das/users-list.html', context)


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def user_add_view(req):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'user_mgr'
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            role = form.cleaned_data['role']
            is_active = form.cleaned_data['is_active']
            if not is_active:
                is_active = 0
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            nickname = form.cleaned_data['nickname']
            avatar = form.cleaned_data['avatar']

            user = auth.authenticate(username=username, password=password, email=email)
            if user:
                context['user'] = user
                context['msg'] = "用户已经存在"
                return render(req, 'das/msg.html', context)
            if role == 'access_all':
                user = User.objects.create(username=username, password=password, email=email, telephone=telephone,
                                           is_active=is_active, first_name=first_name, is_superuser=1,
                                           last_name=last_name, nickname=nickname, avatar=avatar)
            else:
                user = User.objects.create(username=username, password=password, email=email, telephone=telephone,
                                       is_active=is_active, first_name=first_name,
                                       last_name=last_name, nickname=nickname, avatar=avatar)
            user.save()
            perm = Permission.objects.get(codename=role)
            user.user_permissions.add(perm)
            context['msg'] = '用户添加成功'
            return redirect('/das/user/list/1/2', context)
        else:
            context['msg'] = '表单错误'
            return render(req, 'das/msg.html', context)
    return render(req, 'das/user-add.html', context)


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def user_del_view(req, user_id):
    context = {}
    context['active'] = 'user_mgr'
    user = None
    oper_user = req.session.get('user')
    try:
        user = User.objects.get(pk=user_id)
        if oper_user == user:
            context['msg'] = '用户不能删除自己'
            context['result'] = 'failure'
            return HttpResponse(json.dumps(context), content_type="application/json")
        if user.is_superuser and oper_user.is_superuser != 1:
            context['msg'] = '当前用户非超级管理员，不能删除超级管理员账户'
            context['result'] = 'failure'
            return HttpResponse(json.dumps(context), content_type="application/json")
        if oper_user.is_superuser != 1 and user.has_perm('das.access_dashboard'):
            context['msg'] = '非超级管理员不能删除普通管理员账户'
            context['result'] = 'failure'
            return HttpResponse(json.dumps(context), content_type="application/json")
        user.delete()
        context['msg'] = '用户删除成功'
        context['result'] = 'success'
    except:
        context['msg'] = '用户不存在'
        context['result'] = 'failure'
    finally:
        return HttpResponse(json.dumps(context), content_type="application/json")


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def user_modify_view(req, user_id):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'user_mgr'
    try:
        user = User.objects.get(pk=user_id)
    except:
        context['msg'] = '用户不存在'
        return render(req, 'das/msg', context)
    oper_user = req.session.get('user')
    if user.is_superuser and oper_user.is_superuser != 1:
        context['msg'] = '当前用户非超级管理员，不能编辑超级管理员账户'
        context['result'] = 'failure'
        return render(req, 'das/msg.html', context)
    if oper_user.is_superuser != 1 and user.has_perm('das.access_dashboard'):
        context['msg'] = '非超级管理员不能编辑普通管理员账户'
        context['result'] = 'failure'
        return render(req, 'das/msg.html', context)
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            is_active = form.cleaned_data['is_active']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            nickname = form.cleaned_data['nickname']
            avatar = form.cleaned_data['avatar']
            role = form.cleaned_data['role']
            if password:
                user.set_password(password)
            user.email = email
            user.telephone = telephone
            if is_active:
                user.is_active = is_active
            else:
                user.is_active = 0
            user.first_name = first_name
            user.last_name = last_name
            user.nickname = nickname
            user.avatar = avatar
            if role == 'access_all':
                user.is_superuser = 1
            else:
                user.is_superuser = 0
            user.save()
            user.user_permissions.clear()
            perm = Permission.objects.get(codename=role)
            user.user_permissions.add(perm)
            context['msg'] = '用户修改成功'
            return redirect('/das/user/list/1/2', context)
        else:
            context['msg'] = '表单错误'
            return render(req, 'das/msg.html', context)

    context['user'] = user

    return render(req, 'das/user-modify.html', context)


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def user_enable_disable(req, user_id):
    user = User.objects.get(pk=user_id)
    oper_user = req.session.get('user')
    if user.is_superuser and oper_user.is_superuser != 1:
        ret = {'result': 'failure', 'msg': '当前用户非超级管理员，不能操作超级管理员账户'}
        return HttpResponse(json.dumps(ret), content_type="application/json")
    if oper_user.is_superuser != 1 and user.has_perm('das.access_dashboard'):
        ret = {'result': 'failure', 'msg': '非超级管理员不能操作普通管理员账户'}
        return HttpResponse(json.dumps(ret), content_type="application/json")
    if user.is_active == 1:
        user.is_active = 0
        msg = '用户禁用成功'
    else:
        user.is_active = 1
        msg = '用户启用成功'
    user.save()
    ret = {'result': 'success', 'user_status': user.is_active, 'msg': msg}
    return HttpResponse(json.dumps(ret), content_type="application/json")


@login_required(login_url='/login.html')
def user_profile(req):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'user_profile'
    user = req.session.get('user')
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            nickname = form.cleaned_data['nickname']
            avatar = form.cleaned_data['avatar']
            if password:
                user.set_password(password)
            user.email = email
            user.telephone = telephone
            user.first_name = first_name
            user.last_name = last_name
            user.nickname = nickname
            user.avatar = avatar
            user.save()
            req.session['user'] = user
            context['msg'] = '用户修改成功'
            return redirect('/das/', context)
        else:
            context['msg'] = '表单错误'
            return render(req, 'das/msg.html', context)

    context['user'] = user

    return render(req, 'das/user-profile.html', context)


def find_user(req, username_or_email_or_telephone):
    q = Q()
    q.connector = 'OR'
    q.children.append(('username', username_or_email_or_telephone))
    q.children.append(('email', username_or_email_or_telephone))
    q.children.append(('telephone', username_or_email_or_telephone))
    user = User.objects.filter(q)
    if user:
        ret = {'result': 'true'}
    else:
        ret = {'result': 'false'}
    return HttpResponse(json.dumps(ret), content_type="application/json")


@permission_required('das.access_dashboard', login_url='/login.html')
@login_required(login_url='/login.html')
def find_other_user(req, username, email_or_telephone):
    q = Q()
    q.connector = 'OR'
    q.children.append(('email', email_or_telephone))
    q.children.append(('telephone', email_or_telephone))
    user = User.objects.filter(q)
    if user and user[0].username != username:
        ret = {'result': 'true'}
    else:
        ret = {'result': 'false'}
    return HttpResponse(json.dumps(ret), content_type="application/json")


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def menu_view(req):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'menu'
    menus = Menu.objects.filter(menu_type='menu')
    if req.method == 'POST':
        if req.POST.get('menu_id') == '0':
            menu = None
        else:
            menu = Menu.objects.get(pk=req.POST.get('menu_id'))
    else:
        if menus:
            menu = menus[0]
        else:
            menu = None
    pages = Article.objects.filter(article_type='page')
    nodes = Category.objects.get_queryset()
    tags = Tag.objects.all()
    menu_positions = Menu_position.objects.all()
    context['current_menu'] = menu
    try:
        current_menu_option = menu.menu.filter(parent=None).order_by('option_level')
    except:
        current_menu_option = None
    context['current_menu_option'] = current_menu_option
    # a = menu.menu.order_by('option_level')
    # for b in a:
    #     if b.children.all():
    #
    #         for c in b.children.all():
    #             print(c.pk)
    context['menus'] = menus
    context['pages'] = pages
    context['nodes'] = nodes
    context['tags'] = tags
    context['menu_positions'] = menu_positions
    return render(req, 'das/menu.html', context)


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def menu_add(req):
    if req.method == 'POST':
        form = MenuForm(req.POST)
        if form.is_valid():
            menu_name = form.cleaned_data['menu_name']
            menu_type = form.cleaned_data['menu_type']
            menu = Menu.objects.create(menu_name=menu_name, menu_type=menu_type)
            menu.save()
            ret = {'result': 'success', 'menu_name': menu.menu_name, 'menu_id': menu.pk}
            return HttpResponse(json.dumps(ret), content_type="application/json")
        else:
            ret = {'result': 'failure', 'msg': '表单不合法'}
            return HttpResponse(json.dumps(ret), content_type="application/json")
    else:
        ret = {'result': 'failure', 'msg': '非法请求'}
        return HttpResponse(json.dumps(ret), content_type="application/json")


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def menu_del(req, id):
    context = {}
    try:
        menu = Menu.objects.get(pk=id)
        menu.delete()
        return redirect('/das/menu')
    except:
        context['msg'] = '菜单删除失败'
        return render(req, 'das/msg.html', context)


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def menu_modify(req, id):
    try:
        menu = Menu.objects.get(pk=id)
        if req.method == 'POST':
            datas = json.loads(req.body)
            menu.menu_name = datas['menu_name']
            menu.menu_type = datas['menu_type']
            menu.save()
            position_ids = datas['position_ids']

            old_position_ids = []
            for pos in menu.menu_position.all():
                old_position_ids.append(pos.pk)
            if position_ids:
                menu.menu_position.clear()
                for position_id in position_ids:
                    menu_position = Menu_position.objects.get(pk=position_id)
                    menu.menu_position.add(menu_position)
                    menu.save()
            ret = {'result': 'success', 'msg': '菜单修改成功', 'menu_id': menu.pk, 'menu_name': menu.menu_name,
                   'position_ids': position_ids, 'old_position_ids': old_position_ids}
            return HttpResponse(json.dumps(ret), content_type="application/json")
        else:
            ret = {'result': 'failure', 'msg': '非法请求'}
            return HttpResponse(json.dumps(ret), content_type="application/json")
    except:
        ret = {'result': 'failure', 'msg': '菜单不存在'}
        return HttpResponse(json.dumps(ret), content_type="application/json")


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def tool_view(req):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'tool'
    menus = Menu.objects.filter(menu_type='tool')
    menu_option_templates = Menu_option_template.objects.all()
    context['menu_option_templates'] = menu_option_templates
    user_menus = Menu.objects.filter(menu_type='menu')
    context['menus'] = menus
    context['user_menus'] = user_menus
    return render(req, 'das/tool.html', context)


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def menu_option_add(req):
    context = {}
    context['sitemeta'] = settings.SITEMETA
    context['active'] = 'menu'
    menus = Menu.objects.filter(menu_type='menu')
    if req.method == 'POST':
        form = MenuOptionForm(req.POST)
        if form.is_valid():
            option_name = form.cleaned_data['option_name']
            # option_title = form.cleaned_data['option_title']
            option_titles = req.POST.getlist('option_title')
            # option_value = form.cleaned_data['option_value']
            option_values = req.POST.getlist('option_value')
            option_level = form.cleaned_data['option_level']
            menu_id = form.cleaned_data['menu_id']

            menu = Menu.objects.get(pk=menu_id)
            if menu.menu_type == 'menu':
                for index, value in enumerate(option_values):
                    if option_name == '自定义URL':
                        option_value = value
                        option_title = option_titles[0]
                        original_title = option_title
                    else:
                        option_value = req.scheme + "://" + req.get_host() + value
                    for title in option_titles:
                        t = title.split(':')
                        if value == t[0]:
                            option_title = t[1]
                            original_title = option_title
                    if menu.menu.all():
                        option_level = menu.menu.order_by('-option_level')[0].option_level + 1
                    else:
                        option_level = 1
                    menu_option = Menu_option.objects.create(option_name=option_name, option_title=option_title,
                                                             original_title=original_title,
                                                             option_value=option_value, option_icon='icon-list',
                                                             option_level=option_level, menu=menu)
                    menu_option.save()
                    pages = Article.objects.filter(article_type='page')
                    nodes = Category.objects.get_queryset()
                    tags = Tag.objects.all()
                    context['current_menu'] = menu
                    context['current_menu_option'] = menu.menu.order_by('option_level')
                    context['menus'] = menus
                    context['pages'] = pages
                    context['nodes'] = nodes
                    context['tags'] = tags
            else:
                option_template = form.cleaned_data['option_template']

                if menu.menu.all():
                    option_level = menu.menu.order_by('-option_level')[0].option_level + 1
                else:
                    option_level = 1
                if option_name == '自定义菜单':
                    user_menu = Menu.objects.filter(menu_type='menu')[0]
                else:
                    user_menu = None
                menu_option = Menu_option.objects.create(option_name=option_name, option_title=option_name,
                                                         option_icon='icon-list',
                                                         option_level=option_level, menu=menu, user_menu=user_menu,
                                                         option_template=option_template)
                menu_option.save()

            # return redirect('menu_view', {'menu_id': menu_id})

            ret = {'result': 'success', 'menu_option_id': menu_option.pk}
            return HttpResponse(json.dumps(ret), content_type="application/json")
        else:
            ret = {'result': 'failure', 'msg': '表单不合法'}
            return HttpResponse(json.dumps(ret), content_type="application/json")
            # context['msg'] = '表单错误'
            # return render(req, 'das/msg.html', context)
    else:
        ret = {'result': 'failure', 'msg': '请求不合法'}
        return HttpResponse(json.dumps(ret), content_type="application/json")
        # context['msg'] = '请求非法'
        # return render(req, 'das/msg.html', context)


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def menu_option_modify(req, id):
    menu_option = Menu_option.objects.get(pk=id)
    if req.method == 'POST':
        form = MenuOptionForm(req.POST)
        if form.is_valid():
            option_name = form.cleaned_data['option_name']
            option_title = form.cleaned_data['option_title']
            option_icon = form.cleaned_data['option_icon']
            option_value = form.cleaned_data['option_value']
            menu_id = form.cleaned_data['menu_id']
            user_menu_id = form.cleaned_data['user_menu_id']
            user_menu = None
            if user_menu_id:
                user_menu = Menu.objects.get(pk=user_menu_id)
            menu = Menu.objects.get(pk=menu_id)
            menu_option.option_name = option_name
            menu_option.option_title = option_title
            menu_option.option_icon = option_icon
            menu_option.option_value = option_value
            menu_option.menu = menu
            menu_option.user_menu = user_menu
            menu_option.save()
            ret = {'result': 'success', 'menu_option_id': menu_option.pk, 'option_title': menu_option.option_title,
                   'option_icon': menu_option.option_icon, 'option_value': menu_option.option_value,
                   'option_name': menu_option.option_name}
            return HttpResponse(json.dumps(ret), content_type="application/json")
        else:
            ret = {'result': 'failure', 'msg': '表单不合法'}
            return HttpResponse(json.dumps(ret), content_type="application/json")
    else:
        ret = {'result': 'failure', 'msg': '请求不合法'}
        return HttpResponse(json.dumps(ret), content_type="application/json")


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def menu_option_del(req, id):
    menu_option = Menu_option.objects.get(pk=id)
    if menu_option:
        menu_option.delete()
        ret = {'result': 'success', 'msg': '删除成功'}
        return HttpResponse(json.dumps(ret), content_type="application/json")
    else:
        ret = {'result': 'failure', 'msg': '删除失败'}
        return HttpResponse(json.dumps(ret), content_type="application/json")


# @permission_required('das.access_all', login_url='/login.html')
# @login_required(login_url='/login.html')
# def menu_option_order(req, id, pos):
#     menu_option = Menu_option.objects.get(pk=id)
#     if menu_option:
#         menu_option.option_level = pos
#         menu_option.save()
#         ret = {'result': 'success', 'msg': '排序成功'}
#         return HttpResponse(json.dumps(ret), content_type="application/json")
#     else:
#         ret = {'result': 'failure', 'msg': '排序失败'}
#         return HttpResponse(json.dumps(ret), content_type="application/json")

@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def menu_option_order(req):
    level = 1
    menu_option_ids = json.loads(req.body)
    try:
        for menu_option_id in menu_option_ids:
            if len(menu_option_id) > 1:
                menu_option = Menu_option.objects.get(pk=menu_option_id['id'])
                menu_option.option_level = level
                menu_option.save()
                level = level + 1
                for child_id in menu_option_id['children']:
                    child_option = Menu_option.objects.get(pk=child_id['id'])
                    child_option.option_level = level
                    child_option.parent = menu_option
                    child_option.save()
                    level = level + 1
            else:
                menu_option = Menu_option.objects.get(pk=menu_option_id['id'])
                menu_option.option_level = level
                menu_option.parent = None
                menu_option.save()
                level = level + 1
        ret = {'result': 'success', 'msg': '排序成功'}
        return HttpResponse(json.dumps(ret), content_type="application/json")
    except:
        ret = {'result': 'failure', 'msg': '排序失败'}
        return HttpResponse(json.dumps(ret), content_type="application/json")


@permission_required('das.access_all', login_url='/login.html')
@login_required(login_url='/login.html')
def menu_position_modify(req):
    pass
