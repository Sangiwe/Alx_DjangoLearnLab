from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # recipient is current user; show unread first then read
        return Notification.objects.filter(recipient=self.request.user).order_by('-unread', '-timestamp')


class NotificationMarkReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_object(self):
        notif = super().get_object()
        # ensure recipient-only access
        if notif.recipient != self.request.user:
            raise PermissionDenied("You cannot modify this notification.")
        return notif

    def perform_update(self, serializer):
        serializer.save(unread=False)
