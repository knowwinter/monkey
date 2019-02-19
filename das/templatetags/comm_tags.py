from django import template
from django.utils.encoding import force_text
from das.models import *
register = template.Library()


@register.filter
def if_in(item, url):
    img_tpye = ["jpg", "jpeg", "bmp", "ico", "png", "gif"]
    if item in img_tpye:
        return '<a href="' + url + '" data-rel="colorbox"><img src="' + url + '"  height="100" width="100"/></a>'
    else:
        return ' <label class="btn btn-app btn-purple btn-sm"><i class="icon-cloud-upload bigger-200"></i>Upload</label>'

@register.filter
def get_mediaship_date(id_1, id_2):
    post = Article.objects.get(pk=id_1)
    media = Media.objects.get(pk=id_2)
    ship = Mediaship.objects.get(article=post, media=media)
    mediaship_date = ship.ship_date
    return mediaship_date


@register.filter
def get_perm(perm):
    if perm:
        return perm[0]['name']
    else:
        return None


@register.filter
def order_option(option):
    return option.order_by('option_level')
