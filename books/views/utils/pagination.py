from django.core.paginator import Paginator
from django.utils.functional import cached_property
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class LinkHeaderPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "per_page"
    page_size = 20
    max_page_size = 100

    def get_size(self):
        return self.page.paginator.count

    def get_paginated_response(self, data):
        assert self.page is not None
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        first_url = self.get_first_link()
        last_url = self.get_last_link()

        links = []
        for url, label in (
            (first_url, "first"),
            (previous_url, "prev"),
            (next_url, "next"),
            (last_url, "last"),
        ):
            if url is not None:
                links.append('<{}>; rel="{}"'.format(url, label))

        # Variables are named after the spec of the Content-Ranger header
        range_start = self.page.start_index() - 1
        range_end = self.page.end_index() - 1
        size = self.get_size()
        headers = {
            "Content-Range": f"items: {range_start}-{range_end}/{size}",
            "Access-Control-Expose-Headers": "Content-Range, Link",
        }
        if links:
            headers["Link"] = ", ".join(links)

        return Response(data, headers=headers)

    def get_first_link(self):
        if not self.page.has_previous():
            return None
        else:
            url = self.request.build_absolute_uri()
            return remove_query_param(url, self.page_query_param)

    def get_last_link(self) -> str | None:
        if not self.page.has_next():
            return None
        else:
            url = self.request.build_absolute_uri()
            return replace_query_param(
                url,
                self.page_query_param,
                self.page.paginator.num_pages,
            )


class NoCountPaginator(Paginator):
    """
    This paginator implements several optimizations:
    - values('id') to remove annotations (joins) from the query
    - implements a timeout
    """

    @cached_property
    def count(self):
        return 999_999_999_999


class NoCountHeaderPagination(LinkHeaderPagination):
    django_paginator_class = NoCountPaginator
