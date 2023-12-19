from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
rooms = [
    {'id':1,'name':'Lets Learn Python','instructor':'John Doe','category':'Programming','image':'https://source.unsplash.com/1600x900/?coding'},
    {'id':2,'name':'Lets Learn Java','instructor':'John Doe','category':'Programming','image':'https://source.unsplash.com/1600x900/?coding'},
    {'id':3,'name':'Lets Learn C++','instructor':'John Doe','category':'Programming','image':'https://source.unsplash.com/1600x900/?coding'},
]

def home(request):
    context = {'rooms':rooms}
    return render(request,"home.html",context=context)
    # return HttpResponse("Home Page")

def room(request):
    return render(request,"room.html")
    # return HttpResponse("This is a room")
