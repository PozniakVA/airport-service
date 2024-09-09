from django.urls import path, include
from rest_framework import routers

from airport.views import (
    AirplaneViewSet,
    AirplaneTypeViewSet,
    CrewViewSet,
    AirportViewSet,
    RouteViewSet,
    OrderViewSet,
    FlightViewSet,
    TicketViewSet,
)

router = routers.DefaultRouter()
router.register("airplanes", AirplaneViewSet)
router.register(
    "airplane_types",
    AirplaneTypeViewSet,
    basename="airplane_type"
)
router.register("crew", CrewViewSet)
router.register("airports", AirportViewSet)
router.register("route", RouteViewSet)
router.register("orders", OrderViewSet)
router.register("flights", FlightViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = router.urls

app_name = "airport"
