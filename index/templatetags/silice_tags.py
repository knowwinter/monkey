from django import template
from django.utils.encoding import force_text

register = template.Library()

@register.filter
def silice_content(content, num):
    l = len(content)
    num = int(num)

    if '[!--more--]' in content:
        index = content.index('[!--more--]')
        return content[:index]

    if l <= num:
        return content[:l]

    # video_tag_index = get_index(content, "<video")
    # img_tag_index = get_index(content, "<img")
    # a_tag_index = get_index(content, "<a")
    # pre_tag_index = get_index(content, "<pre")
    tag_list = ['<video', '<img', '<a', '<pre']
    index_list = []
    for tag in tag_list:
        index = get_index(content, tag)
        if index != -1:
            index_list.append(index)
    if not index_list:
        return content[:num]
    max_index = max(index_list)
    min_index = min(index_list)
    if min_index > num:
        return content[:num]
    if max_index < num:
        return content[:max_index]
    return content[:min_index]

def get_index(content, pattern):
    try:
        index = content.index(pattern)
    except:
        index = -1
    finally:
        return index