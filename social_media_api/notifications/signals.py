from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.conf import settings
from posts.models import Like, Comment, Post
from accounts.models import User  # or get_user_model
from .models import Notification

# When a Like is created -> notify post author (unless liker is author)
@receiver(post_save, sender=Like)
def create_notification_on_like(sender, instance, created, **kwargs):
    if not created:
        return
    post = instance.post
    actor = instance.user
    recipient = post.author
    if actor == recipient:
        return
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb='liked',
        target_content_type=ContentType.objects.get_for_model(post),
        target_object_id=post.pk
    )

# When a Comment is created -> notify post author
@receiver(post_save, sender=Comment)
def create_notification_on_comment(sender, instance, created, **kwargs):
    if not created:
        return
    post = instance.post
    actor = instance.author
    recipient = post.author
    if actor == recipient:
        return
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb='commented',
        target_content_type=ContentType.objects.get_for_model(post),
        target_object_id=post.pk
    )

# For follows: when a follow happens we cannot easily catch via model save (we used M2M)
# We'll create a helper function in accounts views to create notification there (below)
