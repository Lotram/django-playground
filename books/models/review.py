from django.db import models

from .book import Book
from .library import Library
from .person import Person


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    reader = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="reviews")
    rating = models.SmallIntegerField()
    comments = models.TextField()
    wrote_at = models.DateTimeField()

    library = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name="reviews"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=0, rating__lte=10), name="valid_rating"
            )
        ]
        # TODO change to library - rating index
        indexes = [models.Index(fields=["rating"], name="review_rating_idx")]

    def __str__(self):
        return f"Review ({self.id})"
