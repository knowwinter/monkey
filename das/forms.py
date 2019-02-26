# -*- coding: utf-8 -*-
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(required=True, max_length=30, error_messages={'required': "用户名不能为空"})
    password = forms.CharField(required=False, max_length=30, error_messages={'required': '密码不能为空'})
    email = forms.EmailField(required=True, error_messages={'required': '邮箱不能为空'})
    telephone = forms.CharField(max_length=11, required=False)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    is_active = forms.IntegerField(max_value=2, min_value=0, required=False)
    nickname = forms.CharField(max_length=32, required=False)
    avatar = forms.CharField(max_length=100, required=False)
    role = forms.CharField(required=False)



class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=30, error_messages={'required': "用户名不能为空"})
    password = forms.CharField(required=True, max_length=30, error_messages={'required': '密码不能为空'})


class CateForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, error_messages={'required': "分类名称不能为空"})
    parent = forms.IntegerField(required=True)
    description = forms.CharField(max_length=80)
    url_slug = forms.CharField(max_length=80)


class PostForm(forms.Form):
    title = forms.CharField(max_length=30, required=True, error_messages={'required': "文章标题不能为空"})
    content = forms.CharField(widget=forms.Textarea, required=False)
    # url_slug = forms.CharField(max_length=80)
    pub_author = forms.IntegerField(required=True)
    article_status = forms.CharField(max_length=1, required=False)
    comment_status = forms.CharField(max_length=1, required=False)
    article_type = forms.CharField(max_length=30)
    # article_mime_type = forms.CharField(max_length=30)
    category = forms.IntegerField(required=False)
    tags = forms.CharField(required=False)
    # parent = forms.IntegerField(required=False)


class TagForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, error_messages={'required': "分类名称不能为空"})
    description = forms.CharField(max_length=80)
    # url_slug = forms.SlugField(max_length=80)


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=500, required=True)
    user = forms.IntegerField(required=False)
    comment_author = forms.CharField(max_length=30)
    article = forms.IntegerField(required=True)
    parent = forms.IntegerField(required=False)
    comment_author_ip = forms.GenericIPAddressField(required=False)
    comment_author_email = forms.EmailField(required=False)


class CommentStatusForm(forms.Form):
    comment_status = forms.CharField(required=True)


class ArticleStatusForm(forms.Form):
    article_status = forms.CharField(required=True)

class SiteMetaForm(forms.Form):
    site_name = forms.CharField(max_length=30, required=True)
    description = forms.CharField(max_length=100, required=False)
    keywords = forms.CharField(max_length=100, required=False)
    author = forms.CharField(max_length=100, required=True)
    title = forms.CharField(max_length=100, required=False)
    subtitle = forms.CharField(max_length=100, required=False)
    announcement = forms.CharField(max_length=50, required=False)
    favicon = forms.CharField(max_length=255, required=False)
    head_background_img = forms.CharField(max_length=255, required=False)
    author_img = forms.CharField(max_length=255, required=False)
    head_code = forms.CharField(max_length=2000, required=False)
    foot_code = forms.CharField(max_length=2000, required=False)
    is_weibo = forms.CharField(max_length=1, required=False)
    wb_uid = forms.CharField(max_length=15, required=False)
    is_wechat = forms.CharField(max_length=1, required=False)
    wechat_qrcode = forms.CharField(max_length=255, required=False)
    is_qqgroup = forms.CharField(max_length=1, required=False)
    qqgroup_url = forms.CharField(max_length=500, required=False)
    is_twitter = forms.CharField(max_length=1, required=False)
    twitter_id = forms.CharField(max_length=50, required=False)

class MediaForm(forms.Form):
    o_file_name = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=200, required=False)
    alt = forms.CharField(max_length=50, required=False)


class GroupForm(forms.Form):
    name = forms.CharField(max_length=80, required=True)
    members = forms.CharField(required=False)
    perm = forms.CharField(max_length=10, required=True)


class UserStatusForm(forms.Form):
    user_status = forms.CharField(required=True)


class MenuForm(forms.Form):
    menu_name = forms.CharField(max_length=100, required=True)
    menu_type = forms.CharField(max_length=20, required=True)
    position_id = forms.IntegerField(required=False)


class MenuOptionForm(forms.Form):
    option_name = forms.CharField(max_length=100, required=True)
    option_title = forms.CharField(max_length=30, required=False)
    option_value = forms.CharField(max_length=2000, required=False)
    option_icon = forms.CharField(max_length=30, required=False)
    menu_id = forms.IntegerField(required=True)
    user_menu_id = forms.IntegerField(required=False)
    option_level = forms.IntegerField(required=False)
    option_template = forms.CharField(max_length=2000, required=False)


class MenuPositionForm(forms.Form):
    menu_id = forms.IntegerField(required=True)
