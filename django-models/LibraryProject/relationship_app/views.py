from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library

def list_books(request):
      books = Book.objects.all()  # Fetch all book instances from the database
      context = {'books': books}  # Create a context dictionary with book list
      return render(request, 'list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'