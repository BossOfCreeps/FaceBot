from django import template

from main.models import Album

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_albums(context):
    user = context["request"].user
    return Album.objects.filter(user=user).order_by("-datetime") if user.is_authenticated else []