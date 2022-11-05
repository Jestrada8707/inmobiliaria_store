from django import template

from ..models import CustomNav

register = template.Library()


@register.simple_tag()
def get_menu(slug):
    return CustomNav.objects.get(slug=slug)