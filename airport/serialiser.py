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
        fields = ("id", "name", "rows", "seats_in_rows", "airplane_type")


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )

    class Meta:
        model = Airplane
        fields = ("id", "name", "airplane_type")


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=True)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city",)


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


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name",)


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
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
        )


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer(read_only=True)
    airplane = AirplaneDetailSerializer(read_only=True)
    crew = CrewSerializer(read_only=True, many=True)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "seat", "flight", "order",)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "created_at", "user",)
