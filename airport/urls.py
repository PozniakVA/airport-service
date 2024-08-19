from django.urls import path, include
from rest_framework import routers

from airport.views import AirplaneViewSet, AirplaneTypeViewSet, CrewViewSet, AirportViewSet, RouteViewSet

router = routers.DefaultRouter()
router.register("airplanes", AirplaneViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("crew", CrewViewSet)
router.register("airports", AirportViewSet)
router.register("route", RouteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
