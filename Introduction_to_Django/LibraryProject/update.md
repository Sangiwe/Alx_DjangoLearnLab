```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Check update
print(book)
# Expected Output:
# Nineteen Eighty-Four by George Orwell (1949)
```
```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Check update
print(book)
# Expected Output:
# Nineteen Eighty-Four by George Orwell (1949)
```
