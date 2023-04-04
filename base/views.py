from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Room, Message, User, Location
from .forms import RoomForm, MyUserCreationForm, UserForm
import geocoder
from math import sin, cos, sqrt, atan2, radians
# from background_task import background
# from datetime import timedelta

def getLocation():
    g = geocoder.ip('me')
    userLatitude, userLongitude = g.latlng
    location = Location.objects.create(latitude=userLatitude, longitude=userLongitude)
    return location

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

#@background(schedule=timedelta(seconds=20))
def updateUserLocation(request):
    g = getLocation()
    username = request.user.username
    user = User.objects.get(username=username)
    user.location = g
    user.save()

def getRooms(request):
    all_rooms = Room.objects.all()
    rooms = []
    username = request.user.username
    user = User.objects.get(username=username)
    userLat, userLng = user.location.latitude, user.location.longitude
    for room in all_rooms:
        roomLat, roomLng = room.location.latitude, room.location.longitude
        distance = calculate_distance(userLat, userLng, roomLat, roomLng)
        if distance <= room.radius:
            rooms.append(room)
    return rooms


def home(request):
    context = {}
    if request.user.is_authenticated:
        rooms = getRooms(request)
        context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def register(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.location = getLocation()
            user.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)

def room(request, pk):
    global rooms
    if request.user.is_authenticated:
        rooms = getRooms(request)
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            content=request.POST.get('content')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants, 'rooms': rooms}
    return render(request, 'base/room.html', context)

def createroom(request):
    form = RoomForm()
    if request.method == 'POST':
        room = Room.objects.create(
            host=request.user,
            name=request.POST.get('name'),
            location = getLocation(),
            radius=request.POST.get('radius')
        )
        room.participants.add(request.user)
        return redirect('home')

    context = {'form': form}
    return render(request, 'base/createroom.html', context)