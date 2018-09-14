from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import contactForm
#from .forms import DateForm
from .forms import SignUpForm
from .forms import LogInForm

from .models import HotelList, Reservation

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

def login_view(request):
	if request.method == 'POST':
		form = LogInForm(request.POST or None)

		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('home.html')
	else:
		form = LogInForm()
	return render(request, 'login.html', {'form':form})




def logout_view(request):
	if request.method == 'POST':
		logout(request)
		return redirect('home')



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


def reservation_view(request):
	leavereq = Reservation.objects.all()
	return render(request, 'reservation.html', {'leavereq': leavereq})


def mybooking_view(request):
	return render(request, 'mybooking.html', {})