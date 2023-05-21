from books.models import Book


def list_readers_per_book(library_id) -> dict[str, list[str]]:
    """
    Return a dict {book_title: [reader.name]} for a given library
    """
    books = Book.objects.filter(library_id=library_id)
    return {
        book.title: [reader.name for reader in book.readers.all()] for book in books
    }
