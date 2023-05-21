from rest_framework.filters import OrderingFilter

from .simple import ListReviewsView


class OrderedListReviewsView(ListReviewsView):
    filter_backends = (OrderingFilter,)
    ordering_fields = ["wrote_at", "id", "rating"]
    ordering = ["wrote_at"]
