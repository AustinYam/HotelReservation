from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta

# Create your models here.
class HotelList(models.Model):
    ROOM_CHOICES = (
        ('Single_Bed','Single'),
        ('Double_bed','Double'),
    )

    #user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=100, default='')
    room_type = models.CharField(max_length=100, default='', choices=ROOM_CHOICES)
    single_bed = models.IntegerField(default=0)
    double_bed = models.IntegerField(default=0)
    #like = models.ManyToManyField()
    max_number_of_guests = models.IntegerField(default=0)
    image = models.FileField(upload_to='post_img', blank=True)
    description = models.TextField(max_length=500, default='')
    price = models.DecimalField(max_digits=1000, decimal_places=2)

    def __str__(self):
        return self.hotel_name

    def _get_total(self):
        return self.double_bed * self.price

    new_price = property(_get_total)

class Reservation(models.Model):
    # User Information
    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    #room_type = models.CharField(max_length=100, choices=ROOM_CHOICES)
    max_number_of_guests = models.IntegerField(default=0)
    date_in = models.DateField(default=datetime.now().date())
    date_out = models.DateField()
    total_days = models.IntegerField()

    def __str__(self):
        return self.user.username


    def total_days(self):
        return datetime.now().date() - self.date_out

    num_date = property(total_days)

    