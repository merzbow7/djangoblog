from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.handlers.wsgi import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewPostForm, CommentForm, UserCreationFormBootstrap, AuthenticationFormBootstrap
from .models import Post, Comment


class IndexBlogView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.all().prefetch_related('comments')


class SelfBlogView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("blog_login_user")
    model = Post
    template_name = "blog/index.html"
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(user__exact=self.request.user).prefetch_related('comments')


class FeedBlogView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("blog_login_user")
    model = Post
    template_name = "blog/index.html"
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.all().prefetch_related('comments')


def links(request: HttpRequest):
    return render(request, "blog/links.html")


class PostView(DetailView):
    model = Post
    template_name = "blog/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm
        return context

    def post(self, request: HttpRequest, **kwargs):
        bound_form = CommentForm(request.POST)
        if bound_form.is_valid():
            comment = bound_form.save(commit=False)
            comment.post = Post.objects.get(**kwargs)
            comment.user = request.user
            comment.save()
        return redirect('blog_post_url', **kwargs)


class NewPost(LoginRequiredMixin, CreateView):
    form_class = NewPostForm
    template_name = 'blog/create_or_edit_post.html'
    success_url = reverse_lazy('blog_index')

    def post(self, request: HttpRequest, *args, **kwargs):
        bound_form = NewPostForm(request.POST)
        if bound_form.is_valid():
            post = bound_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(post.get_absolute_url())
        return redirect('blog_new_post')


class EditPost(LoginRequiredMixin, UpdateView):
    form_class = NewPostForm
    template_name = 'blog/create_or_edit_post.html'
    queryset = Post.objects


class DeletePost(LoginRequiredMixin, DeleteView):
    queryset = Post.objects
    success_url = reverse_lazy('blog_index')

    def render_to_response(self, context, **response_kwargs):
        object_ = context["object"]
        object_.delete()
        return redirect(self.success_url)


class DeleteComment(LoginRequiredMixin, DeleteView):
    queryset = Comment.objects
    model = Comment

    def render_to_response(self, context, **response_kwargs):
        object_ = context["object"]
        object_url = object_.post.get_absolute_url()
        object_.delete()
        return redirect(object_url)


class RegisterUser(CreateView):
    prefix = "Registration"
    form_class = UserCreationFormBootstrap
    template_name = 'blog/security.html'
    success_url = reverse_lazy('blog_login_user')

    # def get_context_data(self, **kwargs):
    #     contex = super(RegisterUser, self).get_context_data(**kwargs)
    #     return contex


class LoginUser(LoginView):
    prefix = "Login"
    form_class = AuthenticationFormBootstrap
    template_name = 'blog/security.html'
    success_url = reverse_lazy('blog_index')

    def get_success_url(self):
        return reverse_lazy('blog_index')


def logout_user(request: HttpRequest):
    logout(request)
    return redirect('blog_index')