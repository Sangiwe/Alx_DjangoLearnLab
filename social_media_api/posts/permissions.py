# posts/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Allow read-only access to anyone, but write/delete only to the owner/author.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # obj may be Post or Comment with 'author' attr
        return getattr(obj, 'author', None) == request.user
