# -*- coding: utf-8 -*-
from django import forms

class UserForm(forms.Form):
    username = forms.CharField(required=True, max_length=30, error_messages={'required': "用户名不能为空"})
    password = forms.CharField(required=True, max_length=30, error_messages={'required': '密码不能为空'})
    email = forms.EmailField(required=True, error_messages={'required': '邮箱不能为空'})
    telephone = forms.CharField(max_length=11)

    repassword = forms.CharField(max_length=30)

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
    article_status = forms.CharField(max_length=1, required=True)
    comment_status = forms.CharField(max_length=1, required=True)
    article_type = forms.CharField(max_length=30)
    article_mime_type = forms.CharField(max_length=30)
    category = forms.IntegerField(required=True)
    tags = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)
    parent = forms.IntegerField(required=False)


class TagForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, error_messages={'required': "分类名称不能为空"})
    description = forms.CharField(max_length=80)
    # url_slug = forms.SlugField(max_length=80)
