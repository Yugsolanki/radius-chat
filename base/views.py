from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Room, Message, User, Location
from .forms import RoomForm, MyUserCreationForm, UserForm
import geocoder

def getLocation():
    g = geocoder.ip('me')
    userLatitude, userLongitude = g.latlng
    location = Location.objects.create(latitude=userLatitude, longitude=userLongitude)
    return location

def home(request):
    return render(request, 'base/home.html')

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
    return render(request, 'base/login.html', context)

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
    return render(request, 'base/register.html', context)

def room(request):
    return render(request, 'base/room.html')

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