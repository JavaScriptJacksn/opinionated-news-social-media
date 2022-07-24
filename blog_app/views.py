from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post, Poll
from .forms import CommentForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        # For Post model
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
            }
        # Only rendering poll related context if poll exists
        if Poll.objects.filter(post=post).exists():
            queryset_poll = Poll.objects.filter(post=post)
            poll = get_object_or_404(queryset_poll)
            voted = False
            if poll.total_voters.filter(id=self.request.user.id).exists():
                voted = True
            context["voted"] = voted
            context["poll"] = poll
       
        return render(request, "post_detail.html", context)

    def post(self, request, slug, *args, **kwargs):
        # For Post model
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        # Comment Form
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()
        context = {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm(),
            }
        # For Poll model
        if Poll.objects.filter(post=post).exists():
            queryset_poll = Poll.objects.filter(post=post)
            poll = get_object_or_404(queryset_poll)
            voted = False
            if poll.total_voters.filter(id=self.request.user.id).exists():
                voted = True
            context["voted"] = voted
            context["poll"] = poll

        return render(request, "post_detail.html", context)


class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class PostPoll(View):

    def get(self, request, slug):
        # For Post model
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug) 
        # For Poll model
        queryset_poll = Poll.objects.filter(post=post)
        poll = get_object_or_404(queryset_poll)

        return render(request, 'poll_form.html', {
            'post': post,
            'poll': poll,
        })

    def post(self, request, slug):
        # For Post model
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug) 
        # For Poll model
        queryset_poll = Poll.objects.filter(post=post)
        poll = get_object_or_404(queryset_poll)

        choice = request.POST['choice']

        if choice == "option1":
            poll.option1_value += 1
        elif choice == "option2":
            poll.option2_value += 1
        elif choice == "option3":
            poll.option3_value += 1
        elif choice == "option4":
            poll.option4_value += 1

        poll.total_voters.add(request.user)
        poll.save()

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
