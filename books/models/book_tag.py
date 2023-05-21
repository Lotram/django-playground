from django.db import models

from .book import Book
from .library import Library


class BookTag(models.Model):
    class TagName(models.TextChoices):
        """
        If the book is also available in a specific format, the related tag is created
        """

        COMICS = "comics"
        BRAILLE = "braille"
        AUDIO = "audio"
        MOVIE = "movie"
        FRENCH = "french"
        GERMAN = "german"

    library = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name="book_tags"
    )
    # default = None to prevent empty strings
    name = models.CharField(max_length=128, default=None, choices=TagName.choices)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="tags")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_book_tag_per_book", fields=["library_id", "book", "name"]
            )
        ]

    def __str__(self):
        return f"BookTag ({self.id}) {self.name}"
