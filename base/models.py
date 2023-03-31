from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return f"{self.latitude}, {self.longitude}"

class Room(models.Model):
    host = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    radius = models.PositiveIntegerField()
    participants = models.ManyToManyField('User', blank=True, related_name="participants")
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Message(models.Model):
    content = models.CharField(max_length=500)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[0:50]

class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    rooms = models.ManyToManyField(Room, blank=True)
    
    def __str__(self):
        return self.username