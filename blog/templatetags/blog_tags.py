from django import template
from django.urls import reverse
from transliterate.utils import _

register = template.Library()


@register.simple_tag()
def get_links():
    return (
        "https://www.djangoproject.com",
        "https://djbook.ru/rel3.0/",
        "https://django.fun",
    )


@register.filter(name='skip_first')
def skip_first(lst):
    return lst[1:]


@register.simple_tag()
def side_menu():
    return [
        {"href": reverse('blog_new_post'), "bi_class": "bi bi-plus-lg", "name": "New post"},
        {'href': "", 'bi_class': "bi bi-person", 'name': "Profile"},
        {'href': "", 'bi_class': "bi bi-people-fill", 'name': "Subscriptions"},
        {'href': reverse('blog_logout'), 'bi_class': "bi bi-box-arrow-right", 'name': "Exit"},
    ]


@register.simple_tag()
def make_navbar(*args, **kwargs):
    return {
        "main": {'href': reverse('blog_index'), 'name': "Django blogs"},
        "nav":
            [
                {"href": reverse('blog_myblog'), "name": "My blog"},
                {'href': reverse('blog_feed'), 'name': "Feed"},
                {'href': reverse('blog_links'), 'name': "Links"},
            ]
    }


@register.simple_tag()
def dir_tag(obj):
    return dir(obj)


@register.inclusion_tag('blog/tags/_render_form.html')
def render_form(form):
    return {"form": form}


@register.inclusion_tag('blog/tags/_render_full_form.html')
def render_full_form(**kwargs):
    kwargs.setdefault("button", _("Submit"))
    return kwargs


@register.inclusion_tag('blog/tags/_render_security_form.html')
def render_security_form(**kwargs):
    kwargs.setdefault("button", _("Submit"))
    return kwargs
