# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-02-13 23:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    def forwards_func(apps, schema_editor):
        Menu_option_template = apps.get_model("das", "Menu_option_template")
        db_alias = schema_editor.connection.alias
        Menu_option_template.objects.using(db_alias).bulk_create([
            Menu_option_template(option_name=u'分类目录', option_value="index/tool_template/category_temp.html"),
            Menu_option_template(option_name=u'热点文章', option_value="index/tool_template/hot_topic_temp.html"),
            Menu_option_template(option_name=u'近期更新', option_value="index/tool_template/last_topic_temp.html"),
            Menu_option_template(option_name=u'标签墙', option_value="index/tool_template/tag_temp.html"),
            Menu_option_template(option_name=u'自定义菜单', option_value="index/tool_template/user_define_menu_temp.html"),
            Menu_option_template(option_name=u'自定义文本框',
                                 option_value="index/tool_template/user_define_widget_temp.html"),
        ])

    def reverse_func(apps, schema_editor):
        Menu_option_template = apps.get_model("das", "Menu_option_template")
        db_alias = schema_editor.connection.alias
        Menu_option_template.objects.using(db_alias).filter(option_name=u'分类目录').delete(),
        Menu_option_template.objects.using(db_alias).filter(option_name=u'热点文章').delete(),
        Menu_option_template.objects.using(db_alias).filter(option_name=u'近期更新').delete(),
        Menu_option_template.objects.using(db_alias).filter(option_name=u'标签墙').delete(),
        Menu_option_template.objects.using(db_alias).filter(option_name=u'自定义菜单').delete(),
        Menu_option_template.objects.using(db_alias).filter(option_name=u'自定义文本框').delete(),

    dependencies = [
        ('das', '0037_auto_20190213_2342'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
