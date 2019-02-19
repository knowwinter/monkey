from django import template
import random
from django.utils.encoding import force_text
from django.core import serializers

register = template.Library()

@register.filter
def randombtn(btn):
    btn_class = ['btn-primary', 'btn-info', 'btn-success', 'btn-warning', 'btn-danger']
    return random.sample(btn_class, 1)[0]

@register.filter
def randomlabel(label):
    label_class = ['label-info', 'label-primary', 'label-success', 'label-warning', 'label-danger']
    return random.sample(label_class, 1)[0]


@register.filter
def get_user_menu_option(user_menu):
    if user_menu:
        user_menu_option = user_menu.menu.all().order_by('option_level')
    else:
        user_menu_option = None
    return user_menu_option
