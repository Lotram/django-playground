from django.db import models


class Library(models.Model):
    name = models.CharField(max_length=128, default=None)

    class Meta:
        verbose_name_plural = "libraries"

    def __str__(self):
        return f"Library ({self.id}) {self.name}"
