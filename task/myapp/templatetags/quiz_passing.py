from django import template

register = template.Library()

@register.filter
def index(query, index):
    return query[index]

