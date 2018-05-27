from django import template
from django.utils.encoding import force_text

register = template.Library()


@register.filter
def pk_list(ship_set):
    ship_list = []
    for ship in ship_set:
        ship_list.append(ship.user.pk)
    print ship_list
    return ship_list
