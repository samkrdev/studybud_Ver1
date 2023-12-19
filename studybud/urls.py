from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello, Django!")


def room(request):
    return HttpResponse("This is a room")


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", home),
    # path("room/", room),
    path("", include("base.urls")),
]
