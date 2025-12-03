# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Post


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
    """
    ModelForm for creating and updating Post objects.
    The author is set in the view (request.user) so it's excluded from the form.
    """
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your post here...', 'class': 'form-control', 'rows': 10}),
        }
