from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')
            
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')
            
    context = {'page':'login'}
    return render(request, "base/login_register.html",context=context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    context = {}
    return render(request, "base/login_register.html",context=context)

@login_required(login_url='/login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context=context)
    # return HttpResponse("This is a room")

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        print(request.POST)
        # request.get('name')
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context=context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"obj": room}
    return render(request, "base/delete.html", context=context)
