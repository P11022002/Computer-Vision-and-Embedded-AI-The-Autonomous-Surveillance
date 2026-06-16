from django.urls import path

from surveillance_app.consumers import ControlConsumer

websocket_urlpatterns = [
    path("ws/control/", ControlConsumer.as_asgi()),
]
