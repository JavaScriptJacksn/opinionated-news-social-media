from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, Post, Poll


# Comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


# Create Post
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content", "featured_image", "excerpt", "status"]
        widgets = {
            'content': SummernoteWidget(),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError("Title already exists")
        return title


# Create Poll
class PollForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = ['question', 'option1', 'option2', 'option3', 'option4']

    def clean_post(self):
        post = self.cleaned_data['post']
        if Poll.objects.filter(post=post).exists():
            raise forms.ValidationError("Poll for this post alreadt exists")
        return post


# Edit Post
class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "featured_image", "excerpt", "status"]
        widgets = {
            'content': SummernoteWidget(),
        }


# Edit Poll
class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option1', 'option2', 'option3', 'option4']
