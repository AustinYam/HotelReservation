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
from django.db.models import Sum
from django.contrib import messages
from .forms import contactForm
from .forms import SignUpForm
from .forms import LogInForm


from django.views import View
from django.db.models import Q

from .models import HotelList, Room, Reservation,PhotoForTeam,UserProfile

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
		roomtype = request.POST.get('q-room-type')

		if requiredRoomNum and not roomtype:
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
	context = {
		'users':users
	
	}
	return render(request, 'hotellist.html', context)

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
	
		total_single_bed = rooms.filter(RoomType='Single').aggregate(Sum('TotalRooms'))['TotalRooms__sum']
		total_Queen_bed = rooms.filter(RoomType='Queen').aggregate(Sum('TotalRooms'))['TotalRooms__sum']
		total_King_bed = rooms.filter(RoomType='King').aggregate(Sum('TotalRooms'))['TotalRooms__sum']
		total_Master_Suite_bed = rooms.filter(RoomType='Master Suite').aggregate(Sum('TotalRooms'))['TotalRooms__sum']


		total_room = rooms.aggregate(Sum('TotalRooms'))["TotalRooms__sum"]

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
	
	context = {
		'room':users, 
		'thehotel':thehotel,
		'total_single_bed':total_single_bed,
		'total_Queen_bed':total_Queen_bed,
		'total_King_bed':total_King_bed,
		'total_Master_Suite_bed':total_Master_Suite_bed,
		'total_room':total_room
	}
	return render(request, 'booking.html', context)

@login_required(login_url="login")
def reservation_detail_view(request, thehotelid, roomsid):
	user = request.user
	completed = request.POST.get('switch1', None) 
	if completed:
		print("True")
	else:
		print("False")
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

			point = Reservation.objects.filter(user=request.user).aggregate(Sum('stored_pts'))['stored_pts__sum']

			price = Rooms.price

			points = Rooms.reward_points * StayDuration
		
			TotalCost = StayDuration * price
			TotalCost = int(TotalCost)
			required_points = int(TotalCost) 

			if point == None:
				final_result = 0
			else:
				final_result = int(point) - required_points
				if final_result <= -1:
					final_result = 0
				else:
					final_result = final_result

			date_range = Reservation.objects.filter(user=request.user).filter(date_in__lte=Checkout, date_out__gte=Checkin)
			if date_range:
				UserProfile.objects.filter(user=request.user).update(total_reward_points=final_result)

			user_point = UserProfile.objects.filter(user=request.user).aggregate(Sum('total_reward_points'))['total_reward_points__sum']


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

			point = Reservation.objects.filter(user=request.user).aggregate(Sum('stored_pts'))['stored_pts__sum']

			price = Rooms.price

			points = Rooms.reward_points * StayDuration

			TotalCost = StayDuration * price
			TotalCost = int(TotalCost)
			required_points = int(TotalCost) 

			if point == None:
				final_result = 0
			else:
				final_result = int(point) - required_points
				if final_result <= -1:
					final_result = 0
				else:
					final_result = final_result


			date_range = Reservation.objects.filter(user=request.user).filter(date_in__lte=Checkout, date_out__gte=Checkin)
			if date_range:
				UserProfile.objects.filter(user=request.user).update(total_reward_points=final_result)

			user_point = UserProfile.objects.filter(user=request.user).aggregate(Sum('total_reward_points'))['total_reward_points__sum']


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
	
			point = Reservation.objects.filter(user=request.user).aggregate(Sum('stored_pts'))['stored_pts__sum']
			print(point)
			price = Rooms.price
			
			points = Rooms.reward_points * StayDuration

			TotalCost = StayDuration * price
			TotalCost = int(TotalCost)
			required_points = int(TotalCost)
			
			if point == None:
				final_result = 0
			else:
				final_result = int(point) - required_points
				if final_result <= -1:
					final_result = 0
				else:
					final_result = final_result


			date_range = Reservation.objects.filter(user=request.user).filter(date_in__lte=Checkout, date_out__gte=Checkin)
			if date_range:
				UserProfile.objects.filter(user=request.user).update(total_reward_points=final_result)

			user_point = UserProfile.objects.filter(user=request.user).aggregate(Sum('total_reward_points'))['total_reward_points__sum']

	context = {
		'StayDuration': StayDuration, 
		'thehotel':Hotel, 
		'room':Rooms, 
		'roomprice':price,
		'pt':point,
		'userPts':user_point,
		'pts': points,
		'final_result':final_result,
		'required_points': required_points,
		'totalcost':TotalCost, 
		'checkin':Checkin, 
		'checkout':Checkout,
	}
	return render(request, 'reservation.html', context)

def storingData(request, thehotelid, roomid, checkin, checkout, totalcost, pts, required_points, final_result):
	if request.method == "POST":
		
		fullName = request.POST.get('owner')
		numberOnCard = request.POST.get('number-on-card')
		cvv = request.POST.get('cvv')

		user = request.user
		hotel = HotelList.objects.get(id=thehotelid)
		room = Room.objects.get(id=roomid)
		cost = totalcost
		reward_pts = pts

		newReservation = Reservation()
		newReservation.hotel = hotel
		newReservation.room = room
		newReservation.user = user

		if fullName:
			newReservation.first_name = fullName
			newReservation.last_name = fullName
		else:
			newReservation.first_name = user.first_name
			newReservation.last_name = user.last_name

		newReservation.date_in = checkin
		newReservation.date_out = checkout

		newReservation.total_cost = cost
		newReservation.stored_pts = reward_pts
		newReservation.save()

		link = reverse('thanks')
		return HttpResponseRedirect(link)
	else:
		url = reverse('hotel-list')
		return url

def storingPoint(request, thehotelid, roomid, checkin, checkout, pts, required_points, final_result):
	if request.method == "POST":
		
		fullName = request.POST.get('owner')
		numberOnCard = request.POST.get('number-on-card')
		cvv = request.POST.get('cvv')

		user = request.user
		hotel = HotelList.objects.get(id=thehotelid)
		room = Room.objects.get(id=roomid)
		reward_pts = pts

		total_reward_points = int(reward_pts)
		newReservation = Reservation()
		newReservation.hotel = hotel
		newReservation.room = room
		newReservation.user = user

		if fullName:
			newReservation.first_name = fullName
			newReservation.last_name = fullName
		else:
			newReservation.first_name = user.first_name
			newReservation.last_name = user.last_name

		newReservation.date_in = checkin
		newReservation.date_out = checkout

		if total_reward_points >= 250000:
			reward_pts = total_reward_points - 100000
		else:
			if total_reward_points < 0:
				reward_pts = 0
			else:
				reward_pts = total_reward_points - 50000
		newReservation.stored_pts = reward_pts
		newReservation.save()

		link = reverse('thanks')
		return HttpResponseRedirect(link)
	else:
		url = reverse('hotel-list')
		return url

@login_required(login_url="login")
def confirmation(request):
	context = {}
	return render(request, 'thank_you_page.html', context)

@login_required(login_url="login")
def mybooking(request):
	bookings = Reservation.objects.filter(user=request.user)

	FirstDate = request.session['checkin']
	SecDate =  request.session['checkout']

	Checkin = datetime.datetime.strptime(FirstDate, "%m/%d/%Y").date()
	Checkout = datetime.datetime.strptime(SecDate, "%m/%d/%Y").date()

	date_range = Reservation.objects.filter(user=request.user).filter(date_in__lte=Checkout, date_out__gte=Checkin)
	if date_range:
		Reservation.objects.filter(pk__in=date_range.filter(user=request.user).values_list('id', flat=True)[1:]).delete()

	for hotel_name in Reservation.objects.filter(user=request.user).values_list('hotel__hotel_name', flat=True).distinct():
		Reservation.objects.filter(pk__in=Reservation.objects.filter(user=request.user).filter(hotel__hotel_name=hotel_name).values_list('id', flat=True)[1:]).delete()
		
	points = Reservation.objects.filter(user=request.user).aggregate(Sum('stored_pts'))['stored_pts__sum']
	if points:
		new_value = points 
		if new_value <= -1:
			new_value = 0
	else:
		new_value = 0
		
	earning_points = UserProfile.objects.filter(user=request.user).update(total_reward_points=new_value)
	earning_points = UserProfile.objects.filter(user=request.user)

	context = {'booking':bookings, 'points':points, 'earning_points':earning_points}
	return render(request, 'mybooking.html', context)

@login_required(login_url="login")
def cancelbooking(request, id):
	bookings = Reservation.objects.get(id = id)

	point = Reservation.objects.filter(user=request.user).aggregate(Sum('stored_pts'))['stored_pts__sum']

	if point:
		new_value = point - 10000
		if new_value <= -1:
			new_value = 0
	else:
		new_value = 0

	earning_points = UserProfile.objects.filter(user=request.user).update(total_reward_points=new_value)

	bookings.delete()
	link = reverse('mybooking')
	return HttpResponseRedirect(link)


def search(request):
	template = 'hotellist.html'
	query = request.GET.get('sorting')
	print(query)
	users = HotelList.objects.all()
	if query:
		users = HotelList.objects.filter(Q(city__icontains=query) | Q(hotel_name__icontains=query)| Q(address__icontains=query) | Q(zip_code__icontains=query) | Q(room__RoomType__icontains=query) | Q(room__Bed_Option1__icontains=query) | Q(room__Bed_Option2__icontains=query) | Q(room__Bed_Option3__icontains=query) | Q(room__Bed_Option4__icontains=query)).distinct()
	else:
		users = HotelList.objects.all()

	return render(request, template, {'users':users, 'query':query})
