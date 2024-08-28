import pathlib
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from airport_service import settings

def image_path(instance, filename):
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix

    path_at_media = "upload/"
    if isinstance(instance, Airplane):
        path_at_media = "upload/airplanes/"
    elif isinstance(instance, Airport):
        path_at_media = "upload/airports/"

    return pathlib.Path(path_at_media) / pathlib.Path(filename)

class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_rows = models.IntegerField()
    airplane_type = models.ForeignKey(
        "AirplaneType",
        on_delete=models.CASCADE,
        related_name="airplanes"
    )
    image = models.ImageField(null=True, upload_to=image_path)

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
    image = models.ImageField(null=True, upload_to=image_path)

    def __str__(self) -> str:
        return f"{self.name} ({self.closest_big_city})"


class Route(models.Model):
    source = models.ForeignKey(
        "Airport",
        on_delete=models.CASCADE,
        related_name="routes_as_source"
    )
    destination = models.ForeignKey(
        "Airport",
        on_delete=models.CASCADE,
        related_name="routes_as_destination"
    )
    distance = models.FloatField()

    @property
    def route_name(self) -> str:
        return f"{self.source.name} - {self.destination.name}"

    def clean(self) -> None:
        if self.distance <= 0:
            raise ValidationError("The distance must be greater than 0.")

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.source.name} - {self.destination.name}"


class Flight(models.Model):
    route = models.ForeignKey(
        "Route",
        on_delete=models.CASCADE,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        "Airplane",
        on_delete=models.CASCADE,
        related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(
        "Crew",
        related_name="flights"
    )

    def __str__(self) -> str:
        return f"{self.route} - {self.airplane}"


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        "Flight",
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    @staticmethod
    def validate_ticket(row, seat, flight) -> None:
        names = ["rows", "seats_in_rows"]
        for index, value in enumerate([row, seat]):
            max_value = getattr(flight.airplane, names[index])
            if value < 1 or value > max_value:
                raise ValidationError(
                    f"The seat {value} must be between 1 and {max_value}"
                )

    def clean(self) -> None:
        self.validate_ticket(self.row, self.seat, self.flight)

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("row", "seat")

    def __str__(self) -> str:
        return f"{self.order} - {self.flight}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return str(self.created_at)
