from django import template
from django.db.models import Count

from blog.models import Category
register = template.Library()


@register.inclusion_tag('blog/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}

