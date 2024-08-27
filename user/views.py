from rest_framework import generics

from user.serialiser import UserSerializer


class CreateUserViewSet(generics.CreateAPIView):
    serializer_class = UserSerializer
