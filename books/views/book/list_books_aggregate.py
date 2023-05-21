from django.db.models.query import QuerySet
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from books.models import Book
from books.selectors.book.list_books import list_books_aggregate
from books.views.utils.pagination import LinkHeaderPagination


class BookFilter(filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            "release_date": ["gte", "lte", "lt", "gt"],
            "author_id": ["exact", "in"],
            "author__name": ["iexact"],
        }


class ListAnnotatedBooks(GenericAPIView):
    pagination_class = LinkHeaderPagination
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["release_date", "id"]
    ordering = ["release_date"]

    def get_queryset(self, library_id) -> QuerySet:
        return Book.objects.filter(library_id=library_id).select_related(
            "library", "author"
        )

    def get_annotated_page(self, queryset):
        # FIXME: improve this
        annotated = list_books_aggregate(queryset)
        annotated = annotated.values()  # simplified serialization
        return self.paginate_queryset(annotated)

    def get(self, request, library_id: int) -> Response:
        """
        Similar to rest_framework.mixins.ListModelMixin
        with simplified serialization
        """
        queryset = self.filter_queryset(self.get_queryset(library_id))
        page = self.get_annotated_page(queryset)
        return self.get_paginated_response(page)
