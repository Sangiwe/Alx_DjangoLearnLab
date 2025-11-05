from relationship_app.models import Author, Book, Library, Librarian

# -------------------------------
# 1️⃣ Query all books by a specific author
# -------------------------------
# Example: Get all books written by an author named "George Orwell"
author = Author.objects.get(name="George Orwell")
books_by_author = Book.objects.filter(author=author)
print("Books by George Orwell:", [book.title for book in books_by_author])

# -------------------------------
# 2️⃣ List all books in a library
# -------------------------------
# Example: Get all books available in the "Central Library"
library = Library.objects.get(name="Central Library")
books_in_library = library.books.all()
print("Books in Central Library:", [book.title for book in_library])

# -------------------------------
# 3️⃣ Retrieve the librarian for a library
# -------------------------------
# Example: Get the librarian who manages "Central Library"
librarian = library.librarian
print("Librarian for Central Library:", librarian.name)
