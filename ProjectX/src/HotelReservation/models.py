from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.core.validators import RegexValidator, MinValueValidator,MaxValueValidator


# Create your models here.
class HotelList(models.Model):
    #user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    zip_code = models.CharField(max_length=255, default='')
    telephone = models.CharField(max_length=20, blank=True)
    #single_bed = models.IntegerField(default=0)
    #double_bed = models.IntegerField(default=0)
    #max_number_of_guests = models.IntegerField(default=0)
    image = models.FileField(upload_to='post_img', blank=True)
    description = models.TextField(max_length=500, default='')

    class Meta:
        verbose_name_plural = "Hotels"
        ordering = ('hotel_name',)


    def __str__(self):
        return self.hotel_name



class Room(models.Model):
    hotel = models.ForeignKey(HotelList, on_delete=models.CASCADE)
    priorty = models.CharField(max_length=255, default='')
    RoomType = models.CharField(max_length=255, default='')
    Capacity = models.IntegerField(default=0)
    Bed_Option1 = models.CharField(max_length=255, default='', blank=True)
    Bed_Option2 = models.CharField(max_length=255, default='', blank=True)
    Bed_Option3 = models.CharField(max_length=255, default='', blank=True)
    Bed_Option4 = models.CharField(max_length=255, default='', blank=True)
    room_description = models.TextField(max_length=255, default='')
    room_detail1 = models.TextField(max_length=255, default='', blank=True)
    room_detail2 = models.TextField(max_length=255, default='', blank=True)
    room_detail3 = models.TextField(max_length=255, default='', blank=True)
    price = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    image1 = models.FileField(upload_to='post_img', blank=True)
    TotalRooms = models.CharField(max_length=255, default='')
    #reward_points = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Room'
        ordering = ('priorty',)

    def __str__(self):
        return self.RoomType

#class CardNumber(models.Model):
 #   user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE)
  #  full_name = models.CharField(max_length=255, default='')
   # cvv =  models.CharField(max_length=255, default='')
   # card_number = models.CharField(max_length=255, default='')

class PhotoForTeam(models.Model):
    full_name = models.CharField(max_length=255, default='')
    roles = models.CharField(max_length=255, default='')
    roles2 = models.CharField(max_length=255, default='')
    image1 = models.FileField(upload_to='post_img', blank=True)

    def __str__(self):
        return self.full_name

class Reservation(models.Model):
    # User Information
    room = models.ForeignKey(Room, default=None, null=True, on_delete=models.CASCADE)
    hotel = models.ForeignKey(HotelList, default=None, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    #room_type = models.CharField(max_length=100, default='')
    #max_number_of_guests = models.IntegerField(default=0)
    date_in = models.DateField(auto_now_add=False, null=True, blank=True)
    date_out = models.DateField(auto_now=False, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=1000, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = 'Reservation'

    def __str__(self):
        return self.hotel.hotel_name

    