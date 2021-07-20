from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.core import validators
from transliterate.utils import _

from .models import Comment, Post


class CommentFormOld(forms.Form):
    body = forms.CharField(widget=forms.Textarea, max_length=150)
    body.widget.attrs.update({"class": "form-control", "rows": 4})

    def save(self, post):
        return Comment.objects.create(body=self.cleaned_data['body'], post=post)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {'comment': 'Your comment'}
        widgets = {'comment': forms.Textarea(attrs={"class": "form-control", "rows": 3})}


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'post']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'post': forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }


class UserCreationFormBootstrap(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        help_text=validators.validate_email.message,
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={'autofocus': True, "class": "form-control"}),
        }


class AuthenticationFormBootstrap(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True, "class": "form-control"})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
