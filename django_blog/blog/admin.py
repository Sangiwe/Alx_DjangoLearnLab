from django.contrib import admin
from .models import Profile, Post, Comment # Post if exists

admin.site.register(Profile)
# admin.site.register(Post) -- add if you haven't already
admin.site.register(Post)

admin.site.register(Comment)