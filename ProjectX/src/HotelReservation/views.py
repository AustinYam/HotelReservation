from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate, logout


from .forms import contactForm
from .forms import DateForm
from .forms import SignUpForm
from .forms import LogInForm


import smtplib


# Create your views here.
def home(request):
	form = DateForm(request.POST or None)

	if form.is_valid():
		startdateform = form.cleaned_data.get("Start_Date_Form")
		enddateform = form.cleaned_data.get("End_Date_Form")
		numadult = form.cleaned_data.get('num_adult')
		numchildren = form.cleaned_data.get('num_children')

	context = {'form': form}
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

def loginview(request):
	if request.method == 'POST':
		form = LogInForm(request.POST or None)
		if form.is_valid():
			user = form.login(request)
			if user:
				login(request, user)
				return redirect('home')
	else:
		form = LogInForm()
	return render(request, 'login.html', {'form':form})


