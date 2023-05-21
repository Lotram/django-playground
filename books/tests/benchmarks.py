import statistics
import timeit
from datetime import datetime

from django.urls import reverse
from rest_framework.test import APIClient
from rich.console import Console
from rich.table import Table


client = APIClient()


filters = [
    {},
    {"wrote_at__gte": datetime(2022, 1, 1)},
    {"rating__gte": 6},
    {"wrote_at__gte": datetime(2022, 1, 1), "rating__gte": 6},
]

orderings = [
    "id",
    "wrote_at",
    "rating",
    "-id",
    "-wrote_at",
    "-rating",
    "-wrote_at,rating",
]


data_by_url = {
    "simple-list-reviews": [{}],
    "filtered-list-reviews": filters,
    "ordered-list-reviews": [{"ordering": ordering} for ordering in orderings],
    "complete-list-reviews": [
        {**filter_, "ordering": ordering}
        for filter_ in filters
        for ordering in orderings
    ],
}


def setup_table():
    table = Table(title="Endpoint benchmark", show_lines=True)
    table.add_column("endpoint URL")
    table.add_column("Query params")
    table.add_column("Library")
    table.add_column("Mean duration", style="bold cyan")
    table.add_column("Max duration", style="bold green")
    table.add_column("Runs")
    return table


def format_query_params(data):
    return "\n".join(map(lambda item: f"{item[0]}={item[1]}", data.items()))


def add_row(table, url, data, library, results, repeat):
    table.add_row(
        url,
        format_query_params(data),
        str(library),
        f"{statistics.mean(results):.3f} s",
        f"{max(results):.3f} s",
        str(repeat),
    )


def benchmark_list_reviews(url_names, library_ids, repeat=1):
    table = setup_table()
    for url_name in url_names:
        for data in data_by_url[url_name]:
            for library_id in library_ids:
                url = reverse(url_name, args=[library_id])

                results = timeit.repeat(
                    lambda: client.get(url, data or {}), number=1, repeat=repeat
                )

                add_row(table, url, data, library_id, results, repeat)

    console = Console()
    console.print(table)
