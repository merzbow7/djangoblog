from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag('_art_.html')
def article_menu():
    side_menu = {
        "New post": {"icon": "bi-plus-lg", "href": reverse('blog_new_post')},
        "Profile": {"icon": "bi-person", "href": ''},
        "Subscriptions": {"icon": "bi-people-fill", "href": ''},
        "Exit": {"icon": "bi-box-arrow-right", "href": ''},
    }
    return {"side_menu": side_menu}
