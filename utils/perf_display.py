import time
from contextlib import contextmanager

from django.db import connection, reset_queries
from rich import print


def format_duration(duration):
    return f"{duration:.2f}s."


@contextmanager
def perf_counter(message="Total time", time_sql=False, print_sql=False):
    if time_sql:
        reset_queries()

    start_time = time.perf_counter()
    yield

    msg = f"{message}: {format_duration(time.perf_counter() - start_time)}"
    if time_sql:
        msg += f"\nSQL: {total_sql_duration(connection.queries)}"
        if print_sql:
            for query in connection.queries:
                msg += f"\n {' '*6}(duration: {query['time']})   {query['sql'][:1000]}"
    print(msg)


def total_sql_duration(queries):
    return format_duration(sum(float(query["time"]) for query in queries))
