from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from .forms import contactForm
#from .forms import DateForm
from .forms import SignUpForm




from .models import HotelList, Room

from django.contrib.auth.decorators import login_required
import smtplib


# Create your views here.
def home(request):
	context = {}
	templates = 'home.html'
	return render(request, templates, context)

def contact(request):
	title = ''
	form = contactForm(request.POST or None)
	confirm_message = None
	
	if form.is_valid():
		#print (form.cleaned_data['Email'])
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

	context = {'title': title, 'form':form, 'confirm_message':confirm_message, }
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
	all_hotel_views = HotelList.objects.all()

	page = request.GET.get('page', 1)

	# Limitation 
	paginator = Paginator(all_hotel_views, 3)

	# Check to see whether or not the page is an integer.
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)

	return render(request, 'hotellist.html', {'users':users})

@login_required(login_url="login")
def booking_room_view(request, pk):
	
	if pk:
		thehotel = HotelList.objects.get(pk=pk)
		room = Room.objects.filter(hotel=thehotel)

		page = request.GET.get('page', 1)
		
		# Limitation 
		paginator = Paginator(room, 3)

		# Check to see whether or not the page is an integer.
		try:
			rooms = paginator.page(page)
		except PageNotAnInteger:
			rooms = paginator.page(1)
		except EmptyPage:
			rooms = paginator.page(paginator.num_pages)
	
	return render(request, 'booking.html', {'room':rooms, 'thehotel':thehotel})

def reservation_view(request):
	templates = ''
	context = {''}
	return render(request, templates, context)
