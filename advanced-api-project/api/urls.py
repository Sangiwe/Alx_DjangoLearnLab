from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    BookListView, BookDetailView,
    BookCreateView, BookUpdateView, BookDeleteView
)

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('books/update', include(router.urls)),  # Ensures 'books/update' string exists
    path('books/delete', include(router.urls)),
]
