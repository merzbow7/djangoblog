"""djangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() fpagesunction: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.decorators.cache import cache_page

from blog import views

urlpatterns = [
    path('', views.IndexBlogView.as_view(), name='blog_index'),
    path('myblog/', views.SelfBlogView.as_view(), name='blog_myblog'),
    path('feed/', views.FeedBlogView.as_view(), name='blog_feed'),
    path('links/', cache_page(60 * 300)(views.links), name='blog_links'),
    path('new_post/', views.NewPost.as_view(), name='blog_new_post'),

    path('subscribers/', views.SubscribersView.as_view(), name='blog_subscribers'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='blog_profile'),

    path('edit_post/<slug:slug>', views.EditPost.as_view(), name='blog_edit_post'),
    path('post/<slug:slug>', views.PostView.as_view(), name='blog_post_url'),
    path('post_delete/<slug:slug>', views.DeletePost.as_view(), name='blog_delete_post'),
    path('comment_delete/<slug:slug>', views.DeleteComment.as_view(), name='blog_delete_comment'),

    path('registration/', views.RegisterUser.as_view(), name='blog_register_user'),
    path('login/', views.LoginUser.as_view(), name='blog_login_user'),
    path('logout/', views.logout_user, name='blog_logout'),

]
