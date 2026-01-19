import sys
import os
import django

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    # Clear existing data to ensure a clean slate for sample data creation
    Librarian.objects.all().delete()
    Library.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    # --- Create Sample Data ---

    # Create Authors
    author1 = Author.objects.create(name='J.K. Rowling')
    author2 = Author.objects.create(name='George R.R. Martin')

    # Create Books
    book1 = Book.objects.create(title='Harry Potter and the Sorcerer\'s Stone', author=author1)
    book2 = Book.objects.create(title='A Game of Thrones', author=author2)
    book3 = Book.objects.create(title='Harry Potter and the Chamber of Secrets', author=author1)

    # Create a Library and add books to it
    library1 = Library.objects.create(name='Downtown Library')
    library1.books.add(book1, book2)

    # Create a Librarian for the library
    librarian1 = Librarian.objects.create(name='John Doe', library=library1)

    print("--- Sample Data Created ---")
    print(f"Authors: {Author.objects.count()}")
    print(f"Books: {Book.objects.count()}")
    print(f"Libraries: {Library.objects.count()}")
    print(f"Librarians: {Librarian.objects.count()}")
    print("-" * 20)

    # --- Run Sample Queries ---

    # 1. Query all books by a specific author
    author_name = 'J.K. Rowling'
    print(f"1. Books by {author_name}:")
    retrieved_author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=retrieved_author)
    for book in books_by_author:
        print(f"- {book.title}")
    print("-" * 20)

    # 2. List all books in a library
    library_name = 'Downtown Library'
    print(f"2. Books in {library_name}:")
    retrieved_library = Library.objects.get(name=library_name)
    books_in_library = retrieved_library.books.all()
    for book in books_in_library:
        print(f"- {book.title}")
    print("-" * 20)

    # 3. Retrieve the librarian for a library
    print(f"3. Librarian for {library1.name}:")
    librarian_for_library = Librarian.objects.get(library=library1)
    print(f"- {librarian_for_library.name}")
    print("-" * 20)

if __name__ == '__main__':
    run_queries()
