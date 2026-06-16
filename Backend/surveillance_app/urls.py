from django.urls import path

from .views import control_command, health_check

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("control/", control_command, name="control_command"),
]
