# -*- coding: utf-8 -*-
import re

from django.contrib.auth.decorators import login_required

from models import Sitemeta
from django.core.cache import cache

def parseContent(content, pattern):
    result = re.findall(pattern, content, re.S)
    return result


def get_sitemeta(req):
    try:
        sitemeta = Sitemeta.objects.all()[0]
    except:
        return None
    return sitemeta


def cache_sitemeta(change=False):
    print('从redis中查询数据')
    sitemeta = cache.get('sitemeta')
    if sitemeta is None or change == True:
        print('去数据库中查找数据')
        try:
            sitemeta = Sitemeta.objects.all()[0]
        except:
            sitemeta = None
        finally:
            print('将查询到的数据加载到缓存中')
            cache.set('sitemeta', sitemeta)
    return sitemeta
