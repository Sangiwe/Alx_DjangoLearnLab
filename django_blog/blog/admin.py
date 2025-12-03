from django.contrib import admin
from .models import Profile, Post  # Post if exists

admin.site.register(Profile)
# admin.site.register(Post) -- add if you haven't already
admin.site.register(Post)