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
