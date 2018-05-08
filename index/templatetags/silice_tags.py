from django import template
from django.utils.encoding import force_text

register = template.Library()

@register.filter
def silice_content(content, num):
    l = len(content)
    num = int(num)
    try:
        index = content.index('<pre')
        if index < num:
            return content[:index]
        elif l <= num:
            return content[:l]
        else:
            return content[:num]
    except:
        if l <= num:
            return content[:l]
        else:
            return content[:num]
