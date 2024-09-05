from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import (
    AirplaneType,
    Airport,
    Airplane,
    Route,
    Crew,
    Flight,
    Order,
)
from airport.tests.functions_for_creating_objects_and_urls import (
    sample_airplane_type,
    list_url,
    sample_airplane,
    sample_crew,
    sample_airport,
    sample_route,
    sample_flight,
    sample_order,
    sample_ticket,
)


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
