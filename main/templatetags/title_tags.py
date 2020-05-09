from django import template

register = template.Library()


@register.filter
def title(title):
    return (title.split("…"))[0]


@register.filter
def description(title):
    return (title.split("…"))[1:]
