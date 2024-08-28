from datetime import datetime

from django.db.models import F, Value, Count
from django.db.models.functions import Concat
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from airport.models import (
    Airplane,
    AirplaneType,
    Crew,
    Airport,
    Route,
    Order,
    Flight,
    Ticket
)
from airport.serialiser import (
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    AirplaneTypeSerializer,
    CrewSerializer,
    AirportSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    OrderSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    TicketSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
    AirplaneImageSerializer,
    AirportImageSerializer,
)


def get_parameters_from_ints(query_params):
    return [int(str_id) for str_id in query_params.split(",")]


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        if self.action == "upload_image":
            return AirplaneImageSerializer
        return AirplaneSerializer

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name")
        airplane_type = self.request.query_params.get("airplane_type")

        if name:
            queryset = queryset.filter(name__icontains=name)

        if airplane_type:
            airplane_type_ids = get_parameters_from_ints(airplane_type)
            queryset = queryset.filter(airplane_type__id__in=airplane_type_ids)

        return queryset.distinct().order_by("id")

    @action(
        methods=["POST"],
        detail=True,
    )
    def upload_image(self, request, pk=None):
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct().order_by("id")


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    def get_queryset(self):
        queryset = self.queryset
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset.distinct().order_by("id")


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()

    def get_serializer_class(self):
        if self.action == "upload_image":
            return AirportImageSerializer
        return AirportSerializer
    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct().order_by("id")

    @action(
        methods=["POST"],
        detail=True,
    )
    def upload_image(self, request, pk=None):
        airport = self.get_object()
        serializer = self.get_serializer(airport, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        destination = self.request.query_params.get("destination")

        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)

        return queryset.distinct().order_by("id")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related(
        "user",
    ).prefetch_related(
        "tickets__flight__route__source",
        "tickets__flight__route__destination",
        "tickets__flight__airplane",
    )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        created_at = self.request.query_params.get("created_at")
        route = self.request.query_params.get("route")

        if created_at:
            date = datetime.strptime(created_at, "%Y-%m-%d").date()
            queryset = queryset.filter(created_at__date=date)
        if route:
            queryset = queryset.annotate(
                route_name=Concat(
                    F("tickets__flight__route__source__name"),
                    Value(" - "),
                    F("tickets__flight__route__destination__name")
                )
            ).filter(route_name__icontains=route)

        return queryset.distinct().order_by("created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = (
        Flight.objects.all()
        .select_related()
        .prefetch_related("crew")
        .annotate(
            free_seats=(
                    F("airplane__rows")
                    * F("airplane__seats_in_rows")
                    - Count("tickets")
        )))

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    def get_queryset(self):
        queryset = self.queryset
        route = self.request.query_params.get("route")

        if route:
            queryset = queryset.annotate(
                route_name=Concat(
                    F("route__source__name"),
                    Value(" - "),
                    F("route__destination__name"),
                )
            ).filter(route_name__icontains=route)

        return queryset.distinct().order_by("free_seats")


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related()

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "retrieve":
            return TicketDetailSerializer
        return TicketSerializer

    def get_queryset(self):
        queryset = self.queryset
        route = self.request.query_params.get("route")

        if route:
            queryset = queryset.annotate(
                route_name=Concat(
                    F("flight__route__source__name"),
                    Value(" - "),
                    F("flight__route__destination__name"),
                )
            ).filter(route_name__icontains=route)

        return queryset.distinct().order_by("id")
