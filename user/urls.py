from django.urls import path

from user.views import CreateUserViewSet

urlpatterns = [
    path("register/", CreateUserViewSet.as_view(), name="register" ),
]

app_name = "user"
