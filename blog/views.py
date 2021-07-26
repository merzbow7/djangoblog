from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.handlers.wsgi import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewPostForm, CommentForm, UserCreationFormBootstrap, AuthenticationFormBootstrap
from .models import Post, Comment, UserFollowing
from .utils import ConfirmDeleteMixin


class IndexBlogView(ListView):
    template_name = "blog/index.html"
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.all().prefetch_related('comments').select_related('user')


class SelfBlogView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("blog_login_user")
    template_name = "blog/index.html"
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(user__exact=self.request.user).prefetch_related('comments').select_related('user')


class FeedBlogView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("blog_login_user")
    template_name = "blog/index.html"
    paginate_by = 5

    def get_queryset(self):
        posts = Post.objects.filter(user__followers__from_user=self.request.user)
        return posts.prefetch_related('comments').select_related('user')


def links(request: HttpRequest):
    # request.user.is_authenticated
    return render(request, "blog/links.html")


class PostView(DetailView):
    form = CommentForm

    def get_queryset(self):
        return Post.objects.filter(slug__exact=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post__slug__exact=self.kwargs.get("slug")).select_related("user")
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

    def get_queryset(self):
        Post.objects.select_related('user')
        return super().get_queryset()


class DeletePost(LoginRequiredMixin, ConfirmDeleteMixin, DeleteView):

    def get_queryset(self):
        Post.objects.select_related('user')
        return super().get_queryset()


class DeleteComment(LoginRequiredMixin, ConfirmDeleteMixin, DeleteView):
    model = Comment


class RegisterUser(CreateView):
    prefix = "Registration"
    form_class = UserCreationFormBootstrap
    template_name = 'blog/security.html'
    success_url = reverse_lazy('blog_login_user')


class LoginUser(LoginView):
    prefix = "Login"
    form_class = AuthenticationFormBootstrap
    template_name = 'blog/security.html'

    def get_success_url(self):
        return reverse_lazy('blog_index')


def logout_user(request: HttpRequest):
    logout(request)
    return redirect('blog_index')


class SubscribersView(ListView):
    template_name = "blog/subscribers.html"
    context_object_name = 'current_user'

    def get_queryset(self):
        return self.request.user


class ProfileView(DetailView):
    model = User
    template_name = "blog/auth/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            is_follow = UserFollowing.objects.filter(from_user=self.request.user,
                                                     to_user=self.kwargs.get('pk'))
            context["is_follow"] = is_follow
        else:
            context["is_follow"] = False
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        current_pk = self.kwargs.get("pk")
        if 'Subscribe' in request.POST:
            UserFollowing.objects.create(from_user=request.user,
                                         to_user=User.objects.get(pk=current_pk))
        if 'Unsubscribe' in request.POST:
            UserFollowing.objects.get(from_user=request.user,
                                      to_user=User.objects.get(pk=current_pk)).delete()
        return redirect(reverse_lazy('blog_profile', kwargs={"pk": current_pk}))

    def get_queryset(self):
        return User.objects.filter(pk__exact=self.kwargs.get('pk'))
