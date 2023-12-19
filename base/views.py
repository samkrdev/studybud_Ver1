from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from base.models import Room, Topic
from base.forms import RoomForm


# Create your views here.
# rooms = [
#     {'id':1,'name':'Lets Learn Python','instructor':'John Doe','category':'Programming','image':'https://source.unsplash.com/1600x900/?coding'},
#     {'id':2,'name':'Lets Learn Java','instructor':'John Doe','category':'Programming','image':'https://source.unsplash.com/1600x900/?coding'},
#     {'id':3,'name':'Lets Learn C++','instructor':'John Doe','category':'Programming','image':'https://source.unsplash.com/1600x900/?coding'},
# ]


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    # rooms = Room.objects.filter(topic__name__icontains=q)
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {"rooms": rooms, "topics": topics,"room_count":room_count}
    return render(request, "base/home.html", context=context)
    # return HttpResponse("Home Page")


# def room(request):
#     return render(request,"base/room.html")
#     # return HttpResponse("This is a room")


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context=context)
    # return HttpResponse("This is a room")


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        print(request.POST)
        # request.get('name')
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context=context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        print(request.POST)
        # request.get('name')
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context=context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"obj": room}
    return render(request, "base/delete.html", context=context)
