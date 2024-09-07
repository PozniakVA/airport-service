from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

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
from airport.serialiser import (
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    CrewSerializer,
    AirportSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
)

from airport.tests.functions_for_creating_objects_and_urls import (
    sample_airplane_type,
    list_url,
    sample_airplane,
    detail_url,
    sample_crew,
    sample_airport,
    sample_route,
    sample_flight,
    add_free_seats,
    sample_order,
    sample_ticket,
)


class AuthenticatedAirplaneTypeAPITests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_airplane_type(self) -> None:
        sample_airplane_type()
        airplane_type = AirplaneType.objects.all()
        response = self.client.get(list_url("airplane_type"))
        serializer = AirplaneTypeSerializer(airplane_type, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_airplane_type_by_name(self) -> None:
        airplane_type_1 = sample_airplane_type()
        airplane_type_2 = sample_airplane_type(name="Luxury")

        response = self.client.get(
            list_url("airplane_type"),
            {"name": "Luxury"}
        )

        serializer_1 = AirplaneTypeSerializer(airplane_type_1)
        serializer_2 = AirplaneTypeSerializer(airplane_type_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_2.data, response.data)
        self.assertNotIn(serializer_1.data, response.data)

    def test_create_airplane_type_forbidden(self) -> None:
        payload = {"name": "Wide-body"}

        response = self.client.post(list_url("airplane_type"), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedAirplaneAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_airplane(self) -> None:
        sample_airplane()
        airplanes = Airplane.objects.all()
        response = self.client.get(list_url("airplane"))

        serializer = AirplaneListSerializer(airplanes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_airplane(self) -> None:
        airplane = sample_airplane()
        response = self.client.get(detail_url("airplane", airplane.id))

        serializer = AirplaneDetailSerializer(airplane)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_airplane_by_name(self) -> None:

        airplane_1 = sample_airplane()
        airplane_2 = sample_airplane(name="Airbus A320")

        response = self.client.get(
            list_url("airplane"),
            {"name": "Airbus A320"}
        )

        serializer_1 = AirplaneListSerializer(airplane_1)
        serializer_2 = AirplaneListSerializer(airplane_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_1.data, response.data)
        self.assertIn(serializer_2.data, response.data)

    def test_filter_airplane_by_airplane_type_id(self) -> None:

        airplane_1 = sample_airplane()
        airplane_type = sample_airplane_type(name="Luxury")
        airplane_2 = sample_airplane(airplane_type=airplane_type)

        response = self.client.get(
            list_url("airplane"), {"airplane_type": airplane_type.id}
        )

        serializer_1 = AirplaneListSerializer(airplane_1)
        serializer_2 = AirplaneListSerializer(airplane_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_1.data, response.data)
        self.assertIn(serializer_2.data, response.data)

    def test_create_airplane_forbidden(self) -> None:
        payload = {
            "name": "Gulf-stream G650",
            "rows": 8,
            "seats_in_rows": 4,
            "airplane_type": sample_airplane_type(),
        }

        response = self.client.post(list_url("airplane"), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedCrewAPITests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_crew(self) -> None:
        sample_crew()
        crew = Crew.objects.all()
        serializer = CrewSerializer(crew, many=True)

        response = self.client.get(list_url("crew"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_crew_by_first_name(self) -> None:
        crew_1 = sample_crew()
        crew_2 = sample_crew(first_name="user1")

        response = self.client.get(list_url("crew"), {"first_name": "user1"})

        serializer_1 = CrewSerializer(crew_1)
        serializer_2 = CrewSerializer(crew_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_1.data, response.data)
        self.assertIn(serializer_2.data, response.data)

    def test_filter_crew_by_last_name(self) -> None:
        crew_1 = sample_crew()
        crew_2 = sample_crew(last_name="user1")

        response = self.client.get(list_url("crew"), {"last_name": "user1"})

        serializer_1 = CrewSerializer(crew_1)
        serializer_2 = CrewSerializer(crew_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_1.data, response.data)
        self.assertIn(serializer_2.data, response.data)

    def test_create_crew_forbidden(self) -> None:
        payload = {
            "first_name": "Levi",
            "last_name": "Ackerman",
        }

        response = self.client.post(list_url("crew"), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedAirportAPITests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_airport_list(self) -> None:
        sample_airport()
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)

        response = self.client.get(list_url("airport"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_airport_by_name(self) -> None:
        airport_1 = sample_airport()
        airport_2 = sample_airport(name="London Internation")

        response = self.client.get(
            list_url("airport"),
            {"name": "London Internation"}
        )

        serializer_1 = AirportSerializer(airport_1)
        serializer_2 = AirportSerializer(airport_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_1.data, response.data)
        self.assertIn(serializer_2.data, response.data)

    def test_create_airport_forbidden(self) -> None:
        payload = {
            "name": "Tokyo Airport",
            "closest_big_city": "Tokyo",
        }

        response = self.client.post(list_url("airport"), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedRouteAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_routes(self) -> None:
        sample_route()
        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)

        response = self.client.get(list_url("route"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_route(self) -> None:
        route_1 = sample_route()
        serializer = RouteDetailSerializer(route_1)

        response = self.client.get(detail_url("route", route_1.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_route_by_destination(self) -> None:
        route_1 = sample_route()
        airport = sample_airport(
            name="London Internation",
            closest_big_city="London",
        )
        route_2 = sample_route(destination=airport)

        response = self.client.get(
            list_url("route"), {"destination": "London Internation"}
        )

        serializer_1 = RouteListSerializer(route_1)
        serializer_2 = RouteListSerializer(route_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_1.data, response.data)
        self.assertIn(serializer_2.data, response.data)

    def test_create_route_forbidden(self) -> None:
        payload = {
            "source": sample_airport(),
            "destination": sample_airport(
                name="Los Angeles Internation",
                closest_big_city="Los Angeles",
            ),
            "distance": 1000,
        }

        response = self.client.post(list_url("route"), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedFlightAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_flights(self) -> None:
        sample_flight()
        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)

        response = self.client.get(list_url("flight"))

        for index, flight in enumerate(flights):
            add_free_seats(serializer.data[index], flight)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_flight(self) -> None:
        flight = sample_flight()
        serializer = FlightDetailSerializer(flight)
        serializer_expected = add_free_seats(serializer.data, flight)

        response = self.client.get(detail_url("flight", flight.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_expected)

    def test_filter_flight_by_route_name(self) -> None:
        flight_1 = sample_flight()
        airport = sample_airport(
            name="Paris",
            closest_big_city="Paris",
        )
        route = sample_route(source=airport)
        flight_2 = sample_flight(route=route)

        response = self.client.get(
            list_url("flight"), {"route": "Paris - Tokyo Airport"}
        )

        serializer_1 = FlightListSerializer(flight_1)
        serializer_1_expected = add_free_seats(serializer_1.data, flight_1)

        serializer_2 = FlightListSerializer(flight_2)
        serializer_2_expected = add_free_seats(serializer_2.data, flight_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_1_expected, response.data)
        self.assertIn(serializer_2_expected, response.data)

    def test_create_flight_forbidden(self) -> None:
        payload = {
            "route": sample_route(),
            "airport": sample_airport(),
            "departure_time": "2024-09-30T00:00:00Z",
            "arrival_time": "2024-09-01T00:00:00Z",
            "crew": sample_crew(),
        }

        response = self.client.post(list_url("flight"), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedOrderAPITests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_orders(self) -> None:
        sample_order(user=self.user)
        orders = Order.objects.all()
        serializer = OrderListSerializer(orders, many=True)

        response = self.client.get(list_url("order"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_detail_order(self) -> None:
        order = sample_order(user=self.user)
        serializer = OrderDetailSerializer(order)

        response = self.client.get(detail_url("order", order.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_order_by_created_at(self) -> None:
        order_1 = sample_order(user=self.user)

        response = self.client.get(
            list_url("order"),
            {"created_at": "2010-10-10"}
        )

        serializer_1 = OrderListSerializer(order_1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_1.data, response.data["results"])

    def test_filter_order_by_route(self) -> None:

        order_1 = sample_order(user=self.user)
        sample_ticket(order=order_1)

        order_2 = sample_order(user=self.user)
        airport = sample_airport(name="Paris", closest_big_city="Paris")
        route = sample_route(source=airport)
        flight = sample_flight(route=route)
        sample_ticket(row=2, seat=2, flight=flight, order=order_2)

        response = self.client.get(
            list_url("order"), {"route": "Paris - Tokyo Airport"}
        )

        serializer_1 = OrderListSerializer(order_1)
        serializer_2 = OrderListSerializer(order_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_1.data, response.data["results"])
        self.assertIn(serializer_2.data, response.data["results"])

    def test_create_order_not_forbidden(self) -> None:
        flight = sample_flight()
        payload = {
            "tickets": [
                {
                    "row": 3,
                    "seat": 3,
                    "flight": flight.id,
                }
            ]
        }

        response = self.client.post(list_url("order"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthenticatedTicketAPITests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_tickets(self) -> None:
        sample_ticket()
        tickets = Ticket.objects.all()

        serializer = TicketListSerializer(tickets, many=True)

        response = self.client.get(list_url("ticket"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_ticket(self) -> None:
        ticket = sample_ticket()
        serializer = TicketDetailSerializer(ticket)

        response = self.client.get(detail_url("ticket", ticket.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_ticket_by_route(self) -> None:
        ticket_1 = sample_ticket()

        airport = sample_airport(name="Berlin", closest_big_city="Berlin")
        route = sample_route(source=airport)
        flight = sample_flight(route=route)
        ticket_2 = sample_ticket(row=5, seat=5, flight=flight)

        serializer_1 = TicketListSerializer(ticket_1)
        serializer_2 = TicketListSerializer(ticket_2)

        response = self.client.get(
            list_url("ticket"), {"route": "Berlin - Tokyo Airport"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_1.data, response.data)
        self.assertIn(serializer_2.data, response.data)

    def test_create_ticket_forbidden(self) -> None:
        flight = sample_flight()
        payload = {
            "row": 4,
            "seat": 4,
            "flight": flight.id,
        }

        response = self.client.post(
            list_url("ticket"), {"ticket": payload}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
