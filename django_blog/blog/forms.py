# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Post
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
