from django import forms
from .models import Comment, Poll


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
