from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from cloudinary.forms import cl_init_js_callbacks  
from django.template.defaultfilters import slugify
from .models import Post, Poll
from .forms import CommentForm, PostForm, EditForm, PollForm, EditPollForm

# Home page
class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6

# Post detail
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

# Post likes
class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

# Post poll
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

# User profile
class Profile(generic.ListView):
    model = Post
    template_name = "profile.html"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def post(self, request):

        if 'edit' in request.POST:
            slug = request.POST['edit']
            return HttpResponseRedirect(reverse('edit_post', args=[slug]))
        elif 'delete' in request.POST:
            slug = request.POST['delete']
            Post.objects.filter(slug=slug).delete()

        return HttpResponseRedirect(reverse('profile'))

# Create post
class CreatePost(View):

    def get(self, request):
        return render(request, 'create_post.html', {
            'post_form': PostForm,
        })

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            slug = post.slug
            post.save()
            return HttpResponseRedirect(reverse('create_poll', args=[slug]))

        return render(request, 'create_post.html', {'post_form': form})

# Create Poll
class CreatePoll(View):

    def get(self, request, slug):
        return render(request, 'create_poll.html', {
            'poll_form': PollForm,
        })

    def post(self, request, slug):
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            queryset = Post.objects.filter(slug=slug)
            post = get_object_or_404(queryset)
            poll.post = post
            poll.save()
            return HttpResponseRedirect(reverse('profile'))
        return render(request, 'create_poll.html', {'poll_form': form})


# Edit Post
class EditPost(View):

    def get(self, request, slug):
        queryset = Post.objects.filter(slug=slug)
        post_instance = get_object_or_404(queryset)
        form = EditForm(instance=post_instance)
        return render(request, 'create_post.html', {
            'post_form': form,
        })

    def post(self, request, slug):
        queryset = Post.objects.filter(slug=slug)
        post_instance = get_object_or_404(queryset)
        form = EditForm(request.POST, instance=post_instance)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return HttpResponseRedirect(reverse('edit_poll', args=[slug]))

        return render(request, 'edit_post.html', {'post_form': form})

# Edit/Add new Poll
class EditPoll(View):
    def get(self, request, slug):
        # Redirect to add new Poll if one does not exist for post
        queryset = Post.objects.filter(slug=slug)
        post = get_object_or_404(queryset)
        poll_queryset = Poll.objects.filter(post=post)

        if poll_queryset:
            poll = get_object_or_404(poll_queryset)
            form = EditPollForm(instance=poll)
            return render(request, 'edit_poll.html', {
                'edit_poll_form': form,
            })
        else:
            return HttpResponseRedirect(reverse('create_poll', args=[slug]))

    def post(self, request, slug):
        queryset = Post.objects.filter(slug=slug)
        post = get_object_or_404(queryset)
        poll_queryset = Poll.objects.filter(post=post)
        poll_instance = get_object_or_404(poll_queryset)
        form = EditPollForm(request.POST, instance=poll_instance)
        if form.is_valid():
            poll = form.save(commit=False)
            # Rest votes and voter count
            # Ensures no tampering with results
            # E.g. changing names of winning option with losing option
            poll.option1_value = 0
            poll.option2_value = 0
            poll.option3_value = 0
            poll.option4_value = 0
            poll.total_voters.clear()
            poll.save()
            return HttpResponseRedirect(reverse('profile'))
        return render(request, 'edit_poll.html', {
            'edit_poll_form': form
        })
