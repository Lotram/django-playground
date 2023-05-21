from django.db import models

from .library import Library
from .person import Person


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="writings"
    )
    release_date = models.DateField()
    readers = models.ManyToManyField(Person, related_name="readings", through="Review")

    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="books")

    # typing
    library_id: int

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_book_per_library", fields=["library_id", "author", "title"]
            )
        ]
        indexes = [
            models.Index(
                fields=("library", "release_date"), name="book_library_release_date_idx"
            )
        ]

    def __str__(self) -> str:
        return f"Book ({self.id}) {self.title}"
