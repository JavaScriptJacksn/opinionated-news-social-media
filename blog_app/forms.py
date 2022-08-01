from django import forms
from django.shortcuts import get_object_or_404
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content", "featured_image", "excerpt", "status"]

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError("Title already exists")
        return title

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "featured_image", "excerpt", "status"]
