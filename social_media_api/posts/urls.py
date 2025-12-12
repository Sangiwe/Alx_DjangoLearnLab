# posts/urls.py
from rest_framework import routers
from .views import PostViewSet, CommentViewSet
from .views import FeedListView
from .views import PostViewSet, CommentViewSet, like_post, unlike_post, FeedListView

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls

from django.urls import path
urlpatterns += [
    path('feed/', FeedListView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', like_post, name='post-like'),
    path('posts/<int:pk>/unlike/', unlike_post, name='post-unlike'),
]
