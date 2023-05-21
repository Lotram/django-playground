from collections.abc import Iterable
from datetime import datetime
from itertools import islice
from typing import Generic, TypeVar

from django.db import IntegrityError
from django.db.models import Model
from django.utils import timezone
from tqdm import tqdm


ModelType = TypeVar("ModelType", bound=Model)


class BulkCreator(Generic[ModelType]):
    """Helper class to create a bunch of objects in bulk and display progress."""

    start_time: datetime

    def __init__(
        self,
        model: type["ModelType"],
        total: int | None = None,
        batch_size: int = 2_000,
        keep_results: bool = True,
        unit: str | None = None,
        ignore_conflicts: bool = False,
    ) -> None:
        self.model = model
        self._batch: list[ModelType] = []
        self._created: list[ModelType] = []
        self._total_created = 0
        self._total = total
        self.keep_results = keep_results
        self.batch_size = batch_size
        self._unit = unit or f" {self.model.__name__.lower()} "
        self._ignore_conflicts = ignore_conflicts

        assert batch_size > 0

    def __enter__(self) -> "BulkCreator":
        self.start_time = timezone.now()
        return self

    @property
    def results(self) -> list["ModelType"]:
        if not self.keep_results:
            raise RuntimeError("Results were not kept")
        return self._created

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._batch:
            self.flush()

    def add(self, instance: ModelType) -> None:
        self._batch.append(instance)
        if len(self._batch) >= self.batch_size:
            self.flush()

    def add_many(self, instances: Iterable[ModelType]) -> None:
        instances = iter(instances)

        with tqdm(
            total=self._total,
            unit=self._unit,
            # disable=self._total is None or self._total < self.batch_size,
        ) as progress_bar:
            while True:
                chunk_size = self.batch_size - len(self._batch)
                chunk = list(islice(instances, chunk_size))
                self._batch += chunk
                if len(chunk) < chunk_size:
                    break
                self.flush()
                progress_bar.update(len(chunk))

    def flush(self) -> None:
        if len(self._batch) > 0:
            try:
                created = self.model.objects.bulk_create(self._batch)
            except IntegrityError:
                # we cannot just pass _ignore_conflicts to the bulk_create,
                # because otherwise the PK is not set in the model instances
                if not self._ignore_conflicts:
                    raise
            else:
                if self.keep_results:
                    self._created += created
                self._total_created += len(created)
            finally:
                self._batch = []
