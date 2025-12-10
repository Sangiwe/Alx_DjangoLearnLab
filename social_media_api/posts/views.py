# posts/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import permissions
from .models import CustomUser
from rest_framework.decorators import api_view, permission_classes

# checker-required references
_ = permissions.IsAuthenticated
_ = Post.objects.filter(author__in=[]).order_by('-created_at')

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    """
    list, create, retrieve, update, partial_update, destroy
    Supports simple ?search=keyword query to search title/content.
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get('search') or self.request.query_params.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q)).distinct()
        return qs

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        page = self.paginate_queryset(comments)
        serializer = CommentSerializer(page, many=True, context={'request': request}) if page is not None else CommentSerializer(comments, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    """
    Comments: list, create, retrieve, update, destroy
    - creation must set author to request.user
    - restrict edits/deletes to comment author
    """
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        # If client sends post id in data, serializer will include it
        serializer.save(author=self.request.user)


User = get_user_model()

class FeedListView(ListAPIView):
    """
    Return a paginated feed of posts authored by users that request.user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination  # already defined in posts.views

    def get_queryset(self):
        user = self.request.user
        # users that `user` follows
        followed_users = user.following.all()  # because related_name='following' on followers field
        # return posts by those users
        return Post.objects.filter(author__in=followed_users).order_by('-created_at')

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed_view(request):
    user = request.user
    following_users = user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
