from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.serialiser import UserSerializer


class CreateUserViewSet(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
