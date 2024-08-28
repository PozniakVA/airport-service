from django.db import transaction
from rest_framework import serializers

from airport.models import (
    Airplane,
    AirplaneType,
    Airport,
    Route,
    Flight,
    Crew,
    Ticket,
    Order
)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name",)


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_rows", "airplane_type", "image")


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )

    class Meta:
        model = Airplane
        fields = ("id", "name", "airplane_type", "image")


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=True)


class AirplaneImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "image")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city", "image")


class AirportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "image",)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = (
            "id",
            "route_name",
            "source",
            "destination",
            "distance",
        )


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )
    destination = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )


class RouteDetailSerializer(RouteListSerializer):
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)
#

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name",)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight",)
        unique_together = ("row", "seat")

    def validate(self, attrs) -> None:
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"],
        )
        return data


class FlightSerializer(serializers.ModelSerializer):
    free_seats = serializers.IntegerField(read_only=True)
    taken_seats = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="seat",
        source="tickets",
    )
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "free_seats",
            "taken_seats",
        )


class FlightListSerializer(FlightSerializer):
    route = serializers.SlugRelatedField(
        read_only=True,
        slug_field="route_name",
    )
    airplane = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )

    class Meta(FlightSerializer.Meta):
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "free_seats",
            "taken_seats",
        )


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer(read_only=True)
    airplane = AirplaneDetailSerializer(read_only=True)
    crew = CrewSerializer(read_only=True, many=True)


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(read_only=True)


class TicketDetailSerializer(TicketSerializer):
    flight = FlightDetailSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(
        many=True,
        read_only=False,
        allow_null=False,
    )

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(
        many=True,
        read_only=False,
        allow_null=False,
    )


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketDetailSerializer(
        many=True,
        read_only=False,
        allow_null=False,
    )
