from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post, Like
from notifications.models import Notification

User = get_user_model()

class LikeNotificationTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1','u1@example.com','pass')
        self.user2 = User.objects.create_user('user2','u2@example.com','pass')
        self.post = Post.objects.create(author=self.user1, title='t', content='c')
        self.client = APIClient()

    def test_like_creates_notification(self):
        self.client.force_authenticate(self.user2)
        url = reverse('post-like', args=[self.post.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Like.objects.filter(user=self.user2, post=self.post).exists())
        notif = Notification.objects.filter(recipient=self.user1, actor=self.user2, verb='liked').exists()
        self.assertTrue(notif)
