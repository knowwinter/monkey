from django import template
from das.models import Category
from django.utils.encoding import force_text
register = template.Library()


@register.filter
# @register.filter(name="category_tree")
def cate_tree_path(items, separator=' :: '):
    return separator.join(force_text(separator) for i in items)

@register.filter
def cate_tree_level(level, separator='--'):

    return separator.join(force_text(separator) for i in range(level))