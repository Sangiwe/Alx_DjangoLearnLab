# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Post, Tag
from .models import Comment


class UserRegisterForm(UserCreationForm):
    """Extend the default UserCreationForm to include email."""
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    """Form for updating built-in User fields."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating optional Profile model."""
    class Meta:
        model = Profile
        fields = ('bio', 'avatar')


class PostForm(forms.ModelForm):
    # A text field where users enter tags as comma-separated names.
    tag_list = forms.CharField(
        required=False,
        help_text='Enter comma-separated tags (e.g. django, python, tips)',
        widget=forms.TextInput(attrs={'placeholder': 'tags: django, python'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tag_list']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows':10}),
        }

    def __init__(self, *args, **kwargs):
        # If editing an existing instance, prepopulate tag_list
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['tag_list'].initial = ', '.join([t.name for t in instance.tags.all()])

    def save(self, commit=True, *args, **kwargs):
        # Save post first, then handle tags
        post = super().save(commit=commit)
        tag_names = self.cleaned_data.get('tag_list', '')
        # Clean up tag names
        tag_names = [t.strip() for t in tag_names.split(',') if t.strip()]
        # Clear existing tags (for updates)
        post.tags.clear()
        for name in tag_names:
            tag_obj, created = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
            # In case get_or_create by case-insensitive isn't supported directly, fallback:
            if created is False and tag_obj is None:
                tag_obj = Tag.objects.filter(name__iexact=name).first()
                if not tag_obj:
                    tag_obj = Tag.objects.create(name=name)
            post.tags.add(tag_obj)
        return post


class CommentForm(forms.ModelForm):
    """
    Form used to create or edit comments.
    Only the content is editable by users; post & author are set in view.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'class': 'form-control'
            }),
        }
        labels = {
            'content': ''
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) > 2000:
            raise forms.ValidationError("Comment is too long (max 2000 characters).")
        return content
