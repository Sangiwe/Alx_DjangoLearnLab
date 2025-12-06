# blog/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.urls import reverse
from .models import Comment, Post
from .forms import CommentForm


def register(request):
    """
    Handle user registration. On successful registration, log the user in
    and redirect to LOGIN_REDIRECT_URL.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally log them in automatically
            auth_login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('home')  # change 'home' to your desired URL name
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """
    Show and edit profile details for authenticated users.
    Handles both User fields and Profile model if present.
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        # Only create profile_form if Profile model exists
        try:
            profile_instance = request.user.profile
            profile_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=profile_instance
            )
        except Exception:
            profile_form = None

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        user_form = UserUpdateForm(instance=request.user)
        try:
            profile_instance = request.user.profile
            profile_form = ProfileUpdateForm(instance=profile_instance)
        except Exception:
            profile_form = None

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'blog/profile.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # blog/templates/blog/post_list.html
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-published_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['comments'] = self.object.comments.all()
        data['comment_form'] = CommentForm()
        return data


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # redirect to the detail view after successful creation
    # success_url will default to get_absolute_url if you implement it, else override get_success_url

    def form_valid(self, form):
        # set the author to the logged in user before saving
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # ensure author stays the same
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Only allow the original author to update
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'  # used if you open the form standalone
    # we won't use success_url because we redirect to post detail

    def form_valid(self, form):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        form.instance.post = post
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return redirect('post-detail', pk=post.pk)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
