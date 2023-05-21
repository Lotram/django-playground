import statistics
import timeit

from django.core.management.base import BaseCommand
from django.urls import reverse
from rest_framework.test import APIClient
from rich.console import Console
from rich.table import Table

from books.models import Library


class Command(BaseCommand):
    help = "Run benchmark on API endpoints"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            type=str,
            help="url name, as defined in urls.py",
        )

        parser.add_argument(
            "--library-id",
            type=int,
            help="library id to use",
        )
        parser.add_argument(
            "--number", type=int, help="number of executions for each test", default=3
        )

    def handle(self, *args, **options):
        client = APIClient()
        url_name = options["url"]

        # TODO make sure they exists
        alexandria, personal = Library.objects.filter(
            name__in=["Alexandria", "Personal"]
        ).order_by("id")

        table = Table(title="Endpoint benchmark")
        table.add_column("endpoint URL")
        table.add_column("Library")
        table.add_column("Mean duration", style="bold cyan")
        table.add_column("Max duration", style="bold green")
        table.add_column("Runs")

        repeat = options["number"]

        for library in [alexandria, personal]:
            url = reverse(url_name, args=[library.id])
            results = timeit.repeat(lambda: client.get(url), number=1, repeat=repeat)

            table.add_row(
                url,
                str(library),
                f"{statistics.mean(results):.3f} s",
                f"{max(results):.3f} s",
                str(repeat),
            )

        console = Console()
        console.print(table)
