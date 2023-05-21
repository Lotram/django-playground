from django.urls import path

from .views.book.list_books_aggregate import ListAnnotatedBooks
from .views.book.reader_per_book import ListReaderPerBookView
from .views.review import (
    CompleteListReviewsView,
    FilteredListReviewsView,
    ListReviewsView,
    OrderedListReviewsView,
)


urlpatterns = [
    path(
        "books/<int:library_id>/readers-per-book",
        ListReaderPerBookView.as_view(),
        name="list-reader-per-book",
    ),
    path(
        "books/<int:library_id>/aggregate",
        ListAnnotatedBooks.as_view(),
        name="list-books-aggregate",
    ),
    path(
        "reviews/<int:library_id>/simple",
        ListReviewsView.as_view(),
        name="simple-list-reviews",
    ),
    path(
        "reviews/<int:library_id>/filtered",
        FilteredListReviewsView.as_view(),
        name="filtered-list-reviews",
    ),
    path(
        "reviews/<int:library_id>/ordered",
        OrderedListReviewsView.as_view(),
        name="ordered-list-reviews",
    ),
    path(
        "reviews/<int:library_id>/complete",
        CompleteListReviewsView.as_view(),
        name="complete-list-reviews",
    ),
]
