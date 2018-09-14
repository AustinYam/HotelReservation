from django.contrib import admin

# Register your models here.
from .models import HotelList, Reservation


admin.site.register(HotelList)
admin.site.register(Reservation)