from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from decimal import Decimal
from django.contrib import messages
from django.db.models import F

from .forms import contactForm
from .forms import SignUpForm
from .forms import LogInForm


from django.views import View
from django.db.models import Q
from .models import HotelList, Room, Reservation,PhotoForTeam

from django.contrib.auth.decorators import login_required

import smtplib
import datetime

# Create your views here.
def home(request):
	room = HotelList.objects.all()
	photoforteam = PhotoForTeam.objects.all()
	if request.method == "POST":
		checkIn = request.POST.get('checkin')
		checkOut = request.POST.get('checkout')
		if checkIn == checkOut:
			messages.error(request, 'Yo! Cannot do that!')
			return HttpResponseRedirect('home')
		request.session['checkin'] = checkIn
		request.session['checkout'] = checkOut

		requiredRoomNum = request.POST.get('q')

		if requiredRoomNum:
			users = HotelList.objects.filter(room__Capacity__gte=requiredRoomNum).distinct()

			context ={'users':users}
			return render(request, 'hotellist.html', context)
		return redirect('hotel-list')

	context = {'rooms': room, 'photoforteam':photoforteam}
	templates = 'home.html'
	return render(request, templates, context)


def contact(request):
	title = ''
	form = contactForm(request.POST or None)
	confirm_message = None
	
	if form.is_valid():
		fullname = form.cleaned_data.get("Full_Name")
		Message = form.cleaned_data.get("Message")
		subject = 'Message from MYSITE.com'
		message =  "%s %s" %(Message, fullname)
		emailFrom = form.cleaned_data.get("Email")
		emailTo = [settings.EMAIL_HOST_USER]
		send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
		title = "Thanks!"
		confirm_message = "Thanks for the message. We will get right back to you."
		form = None

	context = {'title': title, 'form':form, 'confirm_message':confirm_message}
	templates = 'contact.html'
	return render(request, templates, context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
        	user1 = form.save(commit=False)
        	user1.user = request.user
        	user1.save()
        	username = form.cleaned_data.get('username')
        	raw_password = form.cleaned_data.get('password1')
        	user = authenticate(username=username, password=raw_password)
        	login(request, user)
        	return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def hotellist_view(request):
	users = HotelList.objects.all()

	return render(request, 'hotellist.html', {'users':users})

@login_required(login_url="login")
def booking_room_view(request, pk):
	if pk:
		theuser = request.user

		FirstDate = request.session['checkin']
		SecDate =  request.session['checkout']

	
		Checkin = datetime.datetime.strptime(FirstDate, "%m/%d/%Y").date()
		Checkout = datetime.datetime.strptime(SecDate, "%m/%d/%Y").date()

		thehotel = HotelList.objects.get(pk=pk)
		rooms = Room.objects.filter(hotel=thehotel)

		for room in rooms:
			RoomBooked = Reservation.objects.filter(room=room).filter(date_out__gte=Checkin, date_in__lte=Checkout)
			roomCount = RoomBooked.count()
			roomCount = int(roomCount)
			available = room.TotalRooms
			available = int(available)

			RoomLeft = available - roomCount
			room.spaceleft = RoomLeft
			print("Number of available rooms")
			print(RoomLeft)

		page = request.GET.get('page', 1)
		
		# Limitation 
		paginator = Paginator(rooms, 3)

		# Check to see whether or not the page is an integer.
		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page(1)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)
	
	return render(request, 'booking.html', {'room':users, 'thehotel':thehotel})

@login_required(login_url="login")
def reservation_detail_view(request, thehotelid, roomsid):
	if request.method == 'POST':
		
		checkIn = request.POST.get('checkin')
		checkOut = request.POST.get('checkout')

		if checkIn == '' and checkOut == '':
			FirstDate = request.session['checkin']
			SecDate =  request.session['checkout']

			Checkin = datetime.datetime.strptime(FirstDate, "%m/%d/%Y").date()
			Checkout = datetime.datetime.strptime(SecDate, "%m/%d/%Y").date()

			timedeltaSum = Checkout - Checkin
			StayDuration = timedeltaSum.days

			Hotel = HotelList.objects.get(id = thehotelid)
			Rooms = Room.objects.get(id= roomsid)

			price = Rooms.price
		
			TotalCost = StayDuration * price

		else:

			request.session['checkin'] = checkIn
			request.session['checkout'] = checkOut
			
			FirstDate = request.session['checkin']
			SecDate =  request.session['checkout']

			Checkin = datetime.datetime.strptime(FirstDate, "%m/%d/%Y").date()
			Checkout = datetime.datetime.strptime(SecDate, "%m/%d/%Y").date()

			timedeltaSum = Checkout - Checkin
			StayDuration = timedeltaSum.days


			Hotel = HotelList.objects.get(id = thehotelid)
			Rooms = Room.objects.get(id= roomsid)

			price = Rooms.price
	
			TotalCost = StayDuration * price 
	else:
		if 'checkin' not in request.session and 'checkout' not in request.session:
			return HttpResponseRedirect('/home/')
		else:
			FirstDate = request.session['checkin']
			SecDate =  request.session['checkout']

			Checkin = datetime.datetime.strptime(FirstDate, "%m/%d/%Y").date()
			Checkout = datetime.datetime.strptime(SecDate, "%m/%d/%Y").date()

			timedeltaSum = Checkout - Checkin
			StayDuration = timedeltaSum.days


			Hotel = HotelList.objects.get(id = thehotelid)
			Rooms = Room.objects.get(id= roomsid)

			price = Rooms.price
			
			TotalCost = StayDuration * price

	context = {
		'StayDuration': StayDuration, 
		'thehotel':Hotel, 
		'room':Rooms, 
		'roomprice':price, 
		'totalcost':TotalCost, 
		'checkin':Checkin, 
		'checkout':Checkout,
	}
	return render(request, 'reservation.html', context)

def storingData(request, thehotelid, roomid, checkin, checkout, totalcost):
	if request.method == "POST":
		fullName = request.POST.get('owner')
		numberOnCard = request.POST.get('number-on-card')
		cvv = request.POST.get('cvv')

		user = request.user
		hotel = HotelList.objects.get(id=thehotelid)
		room = Room.objects.get(id=roomid)
		cost = totalcost

		newReservation = Reservation()
		newReservation.hotel = hotel
		newReservation.room = room
		newReservation.user = user
		newReservation.first_name = fullName
		newReservation.last_name = fullName
		newReservation.date_in = checkin
		newReservation.date_out = checkout
		newReservation.total_cost = cost
		newReservation.save()

		link = reverse('thanks')
		return HttpResponseRedirect(link)
	else:
		url = reverse('hotel-list')
		return url

def confirmation(request):
	context = {}
	return render(request, 'thank_you_page.html', context)

def mybooking(request):
	bookings = Reservation.objects.filter(user=request.user)

	for date_in in Reservation.objects.values_list('date_in', flat=True).distinct():
		Reservation.objects.filter(pk__in=Reservation.objects.filter(date_in=date_in).values_list('id', flat=True)[1:]).delete()

		
	context = {'booking':bookings}
	return render(request, 'mybooking.html', context)

def cancelbooking(request, id):
	bookings = Reservation.objects.get(id = id)
	bookings.delete()
	link = reverse('mybooking')
	return HttpResponseRedirect(link)

def search(request):
	template = 'hotellist.html'
	query = request.GET.get('sorting')
	users = HotelList.objects.all()
	if query:
		users = HotelList.objects.filter(Q(city__icontains=query) | Q(hotel_name__icontains=query)| Q(address__icontains=query))
	else:
		users = HotelList.objects.all()

	return render(request, template, {'users':users, 'query':query})
