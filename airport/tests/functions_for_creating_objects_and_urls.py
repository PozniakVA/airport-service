from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from airport.models import (
    AirplaneType,
    Airplane,
    Crew,
    Airport,
    Route,
    Flight,
    Order,
    Ticket,
)


def list_url(model: str):
    return reverse(f"airport:{model}-list")


def detail_url(model: str, id: int):
    return reverse(f"airport:{model}-detail", args=[id])


def add_free_seats(serializer, flight):
    serializer["free_seats"] = (
        flight.airplane.rows
        * flight.airplane.seats_in_rows
        - flight.tickets.count()
    )
    return serializer


def sample_airplane_type(**params):
    defaults = {"name": "Regional"}
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    defaults = {
        "name": "Boeing 777",
        "rows": 10,
        "seats_in_rows": 6,
        "airplane_type": sample_airplane_type(),
        "image": None,
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_crew(**params):
    defaults = {
        "first_name": "test_1",
        "last_name": "test_1",
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_airport(**params):
    defaults = {
        "name": "Test Airport",
        "closest_big_city": "Test City",
    }
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_route(**params):
    defaults = {
        "source": sample_airport(),
        "destination": sample_airport(
            name="Tokyo Airport",
            closest_big_city="Tokyo",
        ),
        "distance": 5000,
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_flight(**params):
    sample_airplane()
    defaults = {
        "route": sample_route(),
        "airplane": sample_airplane(),
        "departure_time": "2024-08-30T00:00:00Z",
        "arrival_time": "2024-09-01T00:00:00Z",
    }
    crew = params.pop("crew", [sample_crew()])
    defaults.update(params)
    flight = Flight.objects.create(**defaults)
    flight.crew.set(crew)

    return flight


def sample_order(**params):
    user, created = get_user_model().objects.get_or_create(
        email="user12@gmail.com",
        password="user12345",
    )
    defaults = {
        "created_at": "2024-08-30T00:00:00Z",
        "user": user,
    }
    defaults.update(params)
    return Order.objects.create(**defaults)


def sample_ticket(**params):
    defaults = {
        "row": 1,
        "seat": 1,
        "flight": sample_flight(),
        "order": sample_order(),
    }
    defaults.update(params)
    return Ticket.objects.create(**defaults)
