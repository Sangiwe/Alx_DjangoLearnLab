from django.contrib import admin
from .models import Book

# Customize how Book appears in the admin interface
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns shown in the list view
    list_filter = ('publication_year', 'author')            # Filter options on the right side
    search_fields = ('title', 'author')                     # Search bar for title and author

