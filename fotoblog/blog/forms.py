from django import forms
from django.contrib.auth import get_user_model

from .models import Photo, Blog


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']


class BlogForm(forms.ModelForm):
    # You can manage multiple separate forms on a single page,
    # by including a hidden field that identifies the form submitted.
    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)  # attached an edit_blog field

    class Meta:
        model = Blog
        fields = ['title', 'content']


class DeleteBlogForm(forms.Form):
    # You can manage multiple separate forms on a single page,
    # by including a hidden field that identifies the form submitted.
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)  # attached an delete_blog field


User = get_user_model()


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']