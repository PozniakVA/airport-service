from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.models import (
    AirplaneType,
    Airport,
    Airplane,
    Route,
    Crew,
    Flight,
    Order,
    Ticket
)

def list_url(model: str):
    return reverse(f"airport:{model}-list")

def sample_airplane_type(**params):
    defaults = {
        "name": "Regional"
    }
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)

def sample_airplane(**params):
    defaults = {
        "name": "Boeing 777",
        "rows": 10,
        "seats_in_rows": 6,
        "airplane_type": sample_airplane_type(),
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)

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
        "distance": 5000
    }
    defaults.update(params)
    return Route.objects.create(**defaults)

def sample_crew(**params):
    defaults = {
        "first_name": "test_1",
        "last_name": "test_1",
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)

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


class AdminAirplaneApiTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@gmail.com",
            password="admin12345",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_airplane(self) -> None:
        airplane_type = sample_airplane_type()
        payload = {
            "name": "Airbus",
            "rows": 15,
            "seats_in_rows": 6,
            "airplane_type": airplane_type.id,
        }
        response = self.client.post(list_url("airplane"), payload)


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        airplane = Airplane.objects.get(id=response.data["id"])

        # creation requires an id, validate the value
        payload["airplane_type"] = airplane_type

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(airplane, key))


class AdminAirplaneTypeApiTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@gmail.com",
            password="admin12345",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_airplane_type(self) -> None:
        payload = {
            "name": "Airbus",
        }

        response = self.client.post(list_url("airplane_type"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        airplane_type = AirplaneType.objects.get(id=response.data["id"])
        self.assertEqual(payload["name"], airplane_type.name)


class AdminAirportApiTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@gmail.com",
            password="admin12345",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_airport(self) -> None:
        payload = {
            "name": "Test Airport",
            "closest_big_city": "Test",
        }

        response = self.client.post(list_url("airport"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        airport = Airport.objects.get(id=response.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(airport, key))


class AdminCrewApiTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@gmail.com",
            password="admin12345",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_crew(self) -> None:
        payload = {
            "first_name": "Levi",
            "last_name": "Ackerman",
        }

        response = self.client.post(list_url("crew"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        crew = Crew.objects.get(id=response.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(crew, key))


class AdminRouteApiTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@gmail.com",
            password="admin12345",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_route(self) -> None:
        airport_1 = sample_airport()
        airport_2 = sample_airport(
            name="London Airport",
            closest_big_city="London",
        )

        payload = {
            "source": airport_1.id,
            "destination": airport_2.id,
            "distance": 1000,
        }

        response = self.client.post(list_url("route"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # creation requires an id, validate the value
        payload["source"] = airport_1
        payload["destination"] = airport_2
        route = Route.objects.get(id=response.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(route, key))

    def test_delete_route_not_allowed(self) -> None:
        route = sample_route()

        response = self.client.delete(list_url("route"), args=[route.id])

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AdminFlightApiTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@gmail.com",
            password="admin12345",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_flight(self) -> None:
        route = sample_route()
        airplane = sample_airplane()
        crew = sample_crew()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2024-08-30T14:32:00Z",
            "arrival_time": "2024-09-01T00:00:00Z",
            "crew": [crew.id],
        }

        response = self.client.post(list_url("flight"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = {
            "route": route,
            "airplane": airplane,
            "departure_time": parse_datetime("2024-08-30T14:32:00Z"),
            "arrival_time": parse_datetime("2024-09-01T00:00:00Z"),
        }
        flight = Flight.objects.get(id=response.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(flight, key))
        self.assertIn(crew, flight.crew.all())

    def test_create_flight_not_allowed(self) -> None:
        flight = sample_flight()

        response = self.client.delete(list_url("flight"), args=[flight.id])

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AdminTicketApiTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@gmail.com",
            password="admin12345",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_delete_ticket_not_allowed(self) -> None:
        ticket = sample_ticket()

        response = self.client.delete(list_url("ticket"), args=[ticket.id])

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AdminOrderApiTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@gmail.com",
            password="admin12345",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_order(self) -> None:
        flight = sample_flight()
        payload = {
            "tickets": [
                {
                    "row": 4,
                    "seat": 1,
                    "flight": flight.id
                }
            ],
        }

        response = self.client.post(list_url("order"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payload = {"row": 4, "seat": 1, "flight": flight}

        order = Order.objects.get(id=response.data["id"])
        ticket = order.tickets.get(id=response.data["tickets"][0]["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(ticket, key))

    def test_delete_order_not_allowed(self) -> None:
        order = sample_order()

        response = self.client.delete(list_url("order"), args=[order.id])

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
