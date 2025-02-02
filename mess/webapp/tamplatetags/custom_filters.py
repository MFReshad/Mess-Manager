from django import template

register = template.Library()

@register.filter
def get_item(queryset, day):
    return queryset.filter(day=day).first()
