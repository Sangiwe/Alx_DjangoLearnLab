# blog/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

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
