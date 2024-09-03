from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class UnauthenticatedAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        ENDPOINTS = [
            "airplane-list",
            "airplane_type-list",
            "crew-list",
            "airport-list",
            "route-list",
            "order-list",
            "flight-list",
            "ticket-list",
        ]
        for endpoint in ENDPOINTS:
            ENDPOINT_URL = reverse(f"airport:{endpoint}")
            response = self.client.get(ENDPOINT_URL)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                f"{endpoint} must request authentication"
            )
