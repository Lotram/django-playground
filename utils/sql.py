from pathlib import Path

from django.db import connection


def toggle_index(index_name: str, active: bool):
    sql_query = Path("../toggle_index.sql").read_text()
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [active, index_name])


def indexes_size(valid_only=True):
    filename = "valid_indexes_size" if valid_only else "all_indexes_size"
    sql_query = Path(f"../{filename}.sql").read_text()
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
