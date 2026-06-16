from django.urls import include, path

urlpatterns = [
    path("api/", include("surveillance_app.urls")),
]
