from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class AdminAirportApiTestCase(TestCase):
    def setUp(self):
        ...