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