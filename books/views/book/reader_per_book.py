from rest_framework.response import Response
from rest_framework.views import APIView

from books.selectors.book.reader_per_book import list_readers_per_book


class ListReaderPerBookView(APIView):
    def get(self, request, library_id: int) -> Response:
        return Response(list_readers_per_book(library_id), 200)
