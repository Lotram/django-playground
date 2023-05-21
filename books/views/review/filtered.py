from django_filters import rest_framework as filters

from books.models import Review

from .simple import ListReviewsView


class ReviewFilter(filters.FilterSet):
    class Meta:
        model = Review
        fields = {
            "wrote_at": ["gte", "lte", "lt", "gt"],
            "rating": ["exact", "gte", "lte", "lt", "gt"],
        }


class FilteredListReviewsView(ListReviewsView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ReviewFilter
