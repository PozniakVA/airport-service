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


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name} ({self.closest_big_city})"


class Route(models.Model):
    source = models.ForeignKey(
        "Airport",
        on_delete=models.CASCADE,
        related_name="routes"
    )
    destination = models.ForeignKey(
        "Airport",
        on_delete=models.CASCADE,
        related_name="routes"
    )
    distance = models.FloatField()

    def clean(self) -> None:
        if self.distance <= 0:
            raise ValidationError("The distance must be greater than 0.")

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.source.name} - {self.destination.name}"
