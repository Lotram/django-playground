from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import Count, OuterRef, Q, QuerySet
from django.db.models.functions import Coalesce

from books.models import Book, BookTag, Review


def list_books_aggregate(book_qs: QuerySet[Book], review_filters: dict | None = None):
    """
    return a list of book objects,
    annotated with a list of tag names, and count of reviews
    """
    review_filters = (
        {}
        if review_filters is None
        else {f"reviews__{key}": value for key, value in review_filters.items()}
    )
    return book_qs.annotate(
        review_count=Count("reviews", filter=Q(**review_filters)),
        tag_names=ArrayAgg("tags__name"),
    )


def list_books_subquery(book_qs: QuerySet[Book], review_filters: dict | None = None):
    return book_qs.annotate(
        review_count=Coalesce(
            Review.objects.filter(book_id=OuterRef("id"), **(review_filters or {}))
            .values("book_id")
            .annotate(count=Count("id"))
            .values("count"),
            0,
        ),
        tag_names=ArraySubquery(
            BookTag.objects.filter(book_id=OuterRef("id")).values("name")
        ),
    )
