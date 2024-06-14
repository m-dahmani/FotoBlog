from django import forms
from .models import Photo, Blog


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
