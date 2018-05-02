from django import template
from django.utils.encoding import force_text

register = template.Library()


@register.filter
# @register.filter(name="category_tree")
def cate_tree_path(items, separator=' :: '):
    return separator.join(force_text(separator) for i in items)


@register.filter
def cate_tree_level(level, separator='--'):
    return separator.join(force_text(separator) for i in range(level))


@register.filter
def is_parent(cate, cate_id):
    if cate.pk == cate_id:
        return 'disabled'
    else:
        return 'selected="selected"' if cate.parent_id == cate_id else ""
