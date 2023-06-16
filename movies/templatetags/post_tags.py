from django import template
from ..views import movie_month

register = template.Library()


@register.simple_tag
def percentage(value, total):
    return round(value / total * 100)


@register.inclusion_tag("movies/account.html")
def show_divisor():
    pass


# @register.simple_tag
# def month(num_month):
#     return movie_month(num_month)
#
#
# @register.inclusion_tag("movies/epic.html")
# def show_divisor():
#     pass
