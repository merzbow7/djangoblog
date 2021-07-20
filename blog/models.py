import time

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.template import defaultfilters
from unidecode import unidecode


class SlugMixin:

    @classmethod
    def create_slug(cls, data: str) -> str:
        slug = defaultfilters.slugify(unidecode(data[:50]))
        while cls.objects.filter(slug__exact=slug).count():
            slug += f"-{int(time.time())}"
        return slug


class Post(SlugMixin, models.Model):
    title = models.CharField(max_length=50, db_index=True)
    post = models.TextField(max_length=500, blank=False, db_index=True)
    slug = models.SlugField(max_length=75, unique=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Записи пользователей'
        verbose_name_plural = 'Записи пользователей'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.create_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_post_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('blog_edit_post', kwargs={'slug': self.slug})

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"


class Comment(SlugMixin, models.Model):
    comment = models.TextField(max_length=150, blank=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    slug = models.SlugField(max_length=75, unique=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарии пользователей'
        verbose_name_plural = 'Комментарии пользователей'

    def save(self, *args, **kwargs):
        self.slug = self.create_slug(self.comment)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.post.get_absolute_url()

    def __repr__(self):
        return f"<Comment {self.id}: {self.comment[:25]}>"
