import time

from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpRequest
from django.template import defaultfilters
from unidecode import unidecode


class ConfirmDeleteMixin:
    template_name = "blog/instance_confirm_delete.html"

    def delete(self, request: HttpRequest, *args, **kwargs):
        """
        delete if user have permissions else 403
        """
        try:
            to_delete = self.model.objects.get(slug__iexact=kwargs.get('slug'))
            if to_delete.user != request.user:
                return HttpResponseForbidden()
        except self.model.DoesNotExist:
            return HttpResponseNotFound()
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_parent_url()


class SlugMixin:

    @classmethod
    def create_slug(cls, data: str) -> str:
        slug = defaultfilters.slugify(unidecode(data[:50]))
        while cls.objects.filter(slug__exact=slug).count():
            slug += f"-{int(time.time())}"
        return slug
