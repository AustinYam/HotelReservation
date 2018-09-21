from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.core.validators import RegexValidator

# Create your models here.
class HotelList(models.Model):
    #user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    zip_code = models.CharField(max_length=255, default='')
    #latitude = models.CharField(max_length=255, default='')
    #longitude = models.CharField(max_length=255, default='')
    telephone = models.CharField(max_length=20, blank=True)
    #single_bed = models.IntegerField(default=0)
    #double_bed = models.IntegerField(default=0)
    max_number_of_guests = models.IntegerField(default=0)
    image = models.FileField(upload_to='post_img', blank=True)
    description = models.TextField(max_length=500, default='')

    class Meta:
        verbose_name_plural = "Hotels"
        ordering = ('hotel_name',)


    def __str__(self):
        return self.hotel_name

class Room(models.Model):
    hotel = models.ForeignKey(HotelList, on_delete=models.CASCADE)
    RoomType = models.CharField(max_length=255, default='')
    Capacity = models.IntegerField(default=0)
    Bed_Option = models.CharField(max_length=255, default='')
    room_description = models.TextField(max_length=255, default='')
    room_detail = models.TextField(max_length=255, default='')
    price = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    image1 = models.FileField(upload_to='post_img', blank=True)
    TotalRooms = models.CharField(max_length=255, default='')

    class Meta:
        verbose_name_plural = 'Room'
        ordering = ('RoomType',)

    def __str__(self):
        return self.RoomType

class Reservation(models.Model):
    # User Information
    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    room_type = models.CharField(max_length=100, default='')
    max_number_of_guests = models.IntegerField(default=0)
    date_in = models.DateField(auto_now_add=True)
    date_out = models.DateField(auto_now=True)
    total_days = models.IntegerField(default=0)
    #check_in = models.DateField(auto_now_add=True)
    #check_out = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username

class BestChoice(models.Model):
    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    hotel = models.ForeignKey(HotelList, on_delete=models.CASCADE)

    def __str__(self):
        return self.hotel.hotel_name

    