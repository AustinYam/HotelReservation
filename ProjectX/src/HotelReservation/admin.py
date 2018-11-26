from django.contrib import admin

# Register your models here.
from .models import HotelList, Reservation, Room, PhotoForTeam, UserProfile

admin.site.register(Room)
admin.site.register(HotelList)
admin.site.register(Reservation)
admin.site.register(PhotoForTeam)