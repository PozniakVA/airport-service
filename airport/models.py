from django.core.exceptions import ValidationError
from django.db import models


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_rows = models.IntegerField()
    airplane_type = models.ForeignKey(
        "AirplaneType",
        on_delete=models.CASCADE,
        related_name="airplanes"
    )

    def clean(self) -> None:
        if self.rows <= 0:
            raise ValidationError("The number of rows must be greater than 0.")
        if self.seats_in_rows <= 0:
            raise ValidationError("The number of seats in rows must be greater than 0.")

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
