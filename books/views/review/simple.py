from django.db.models.query import QuerySet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from books.models import Review
from books.views.utils.pagination import NoCountHeaderPagination


class ListReviewsView(GenericAPIView):
    pagination_class = NoCountHeaderPagination

    def get_queryset(self, library_id) -> QuerySet:
        return Review.objects.filter(library_id=library_id)

    def get(self, request, library_id: int) -> Response:
        """
        Similar to rest_framework.mixins.ListModelMixin
        with simplified serialization
        """
        queryset = self.filter_queryset(self.get_queryset(library_id))
        queryset = queryset.values()  # simplified serialization
        page = self.paginate_queryset(queryset)
        return self.get_paginated_response(page)
