```python
from bookshelf.models import Book

# Retrieve all Book records
books = Book.objects.all()
print(books)
# Expected Output:
# <QuerySet [<Book: 1984 by George Orwell (1949)>]>
```
