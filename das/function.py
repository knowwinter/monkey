# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def display(objs):
    display_list = []

    for obj in objs:
        display_list.append(obj)

        children = obj.children.all()

        if len(children) > 0:
            display_list.append(display(obj.children.all()))
    return display_list
