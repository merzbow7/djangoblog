from django.core.handlers.wsgi import HttpRequest
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse

from .forms import NewPostForm
from .models import Post


class BaseBlogMixin:
    posts = None

    def get(self, request: HttpRequest) -> HttpResponse:
        page_number = request.GET.get('page', 1)
        pages = Paginator(self.posts(), 3)
        page = pages.get_page(page_number)
        context = {"page": page}
        return render(request, "blog/index.html", context=context)


class BasePostMixin:
    header = None
    href = None

    def get_post(self, slug: str):
        return get_object_or_404(Post, slug__iexact=slug) if slug else None

    def get(self, request: HttpRequest, *, slug=None) -> HttpResponse:
        post = self.get_post(slug)
        context = {"form": NewPostForm(instance=post),
                   "header": self.header,
                   "href": reverse(self.href, kwargs={'slug': slug} if slug else None)
                   }
        return render(request, "blog/create_or_edit_post.html", context=context)

    def post(self, request: HttpRequest, *, slug=None) -> HttpResponse:
        old_post = self.get_post(slug)
        bound_form = NewPostForm(request.POST, instance=old_post)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('blog_index')
        else:
            return render(request, "blog/create_or_edit_post.html", context={'form': bound_form})


class DeleteObjectMixin:
    obj = None

    def get(self, request: HttpRequest, slug: str = None) -> HttpResponse:
        item = get_object_or_404(self.obj, slug__iexact=slug)
        item.delete()
        return redirect(request.headers['Referer'])
