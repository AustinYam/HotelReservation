from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.forms.widgets import PasswordInput, TextInput


class contactForm(forms.Form):
	Full_Name = forms.CharField(label='',required=True, max_length=4000, help_text='', widget=forms.TextInput(
		attrs={
			'placeholder': 'Full Name',
			'style': 'font-family: cursive; border: 1px solid #000; border-radius: 5px; width: 770px;',
		}
	))
	Email = forms.EmailField(label='', required=True, widget=forms.TextInput(
		attrs={
			'placeholder': 'Email Address',
			'style': 'font-family: cursive; border: 1px solid #000; border-radius: 5px; width: 770px;',
		}
	))

	Message = forms.CharField(label='', required=True, widget=forms.Textarea(
		attrs={
			'placeholder': 'Message',
			'style': 'font-family: cursive; border: 1px solid #000; border-radius: 5px; width: 770px; height: 300px; resize: none;',
		}
	))

class DateForm(forms.Form):
    Start_Date_Form = forms.DateField(label='', widget=forms.DateInput(attrs={
    	'class':'datepicker',
    	'placeholder': 'Start Date',
    	'style': 'font-family: cursive; width: 250px; font-size: 20px; height: 30px; position: relative; color: #000; border-radius: 10px; border: none; padding: 0 10px; position: relative; top: -50px; left: 89px;',

    }))
    End_Date_Form = forms.DateField(label='', widget=forms.DateInput(attrs={
    	'class':'datepicker',
    	'placeholder': 'End Date',
    	'style': 'font-family: cursive; width: 250px; font-size: 20px; height: 30px; position: relative; color: #000; border-radius: 10px; border: none; padding: 0 10px; position: relative; top: -45px; left: 89px;',

    }))

    Num_Adult = [tuple([x,x]) for x in range(1,21)]
    num_adult = forms.IntegerField(label='', widget=forms.Select(choices=Num_Adult,
    	attrs={
    		'class': 'num_adult',
    		'style': 'font-size: 20px; width: 250px; border: none; font-family: cursive; position: relative; top: -10px; left: 90px; padding: 0 10px;'
    	}
    ))

    Num_Children = [tuple([x,x]) for x in range(1,21)]
    num_children = forms.IntegerField(label='', widget=forms.Select(choices=Num_Children,
    	attrs={
    		'class': 'num_children',
    		'style': 'font-size: 20px; width: 250px; border: none; font-family: cursive; position: relative; top: 35px; left: 90px; padding: 0 10px;'
    	}
    ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False, help_text='', widget=forms.TextInput(
        attrs={
            'style': 'width: 200px;',
        }
    ))
    first_name = forms.CharField(max_length=30, required=False, help_text='')
    last_name = forms.CharField(max_length=30, required=False, help_text='')
    email_address = forms.EmailField(max_length=254, help_text='')
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email_address', 'password1', 'password2',)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class LogInForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ('username', 'password',)    

    def __init__(self, *args, **kwargs):
        super(LogInForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'})
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Password'})


