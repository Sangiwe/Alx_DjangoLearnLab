from django.db import models
from django.contrib.auth.models import User

# The Post model represents a blog post created by a registered user.
# A single user can create many posts — this is a One-to-Many relationship.
class Post(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    published_date = models.DateTimeField(auto_now_add=True)

    # Links each post to the user that created it.
    # related_name='posts' allows us to access user's posts like: user.posts.all()
    author = models.ForeignKey(
        User,
        related_name="posts",
        on_delete=models.CASCADE,
        null=False
    )

    def __str__(self):
        return self.title

        # Optional: helpful for redirecting after create/update if you use get_absolute_url
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post-detail', kwargs={'pk': self.pk})

class Profile(models.Model):
    """Optional: extend default User with extra fields like avatar and bio."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


class Comment(models.Model):
    """
    Comment attached to a Post.
    - post: the Post this comment belongs to (many comments -> one post)
    - author: the User who wrote the comment
    - content: the comment text
    - created_at: timestamp created
    - updated_at: timestamp last updated
    """
    post = models.ForeignKey(
        'Post',
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']   # oldest first; change to '-created_at' if you prefer newest first

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'