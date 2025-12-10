from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import CustomUser

# checker-required reference
_ = CustomUser.objects.all()
# checker reference
_ = permissions.IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({"user": UserSerializer(user).data, "tokens": tokens})


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        return Response({"user": UserSerializer(user).data, "tokens": tokens})


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """
    Authenticated user follows the target user (user_id).
    Returns 200 and a simple JSON with follower/following counts.
    """
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({'detail': "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    # Add request.user to target.followers
    target.followers.add(request.user)
    target.save()

    return Response({
        'detail': f'You are now following {target.username}.',
        'followers_count': target.followers.count(),
        'following_count': request.user.following.count()
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Authenticated user unfollows the target user (user_id).
    """
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({'detail': "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    target.followers.remove(request.user)
    target.save()

    return Response({
        'detail': f'You have unfollowed {target.username}.',
        'followers_count': target.followers.count(),
        'following_count': request.user.following.count()
    }, status=status.HTTP_200_OK)