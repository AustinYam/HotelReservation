from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
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



class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False, help_text='', widget=forms.TextInput(
        attrs={
            'style': 'width: 300px;'
        }
    ))
    first_name = forms.CharField(max_length=30, required=False, help_text='', widget=forms.TextInput(

    ))
    last_name = forms.CharField(max_length=30, required=False, help_text='')
    email_address = forms.EmailField(max_length=254, required=False, widget=forms.TextInput(

    ))
    password1 = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput(

    ))
    password2 = forms.CharField(label='Password Confirmation', max_length=32, widget=forms.PasswordInput())

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

    def email_verify(self):
        if email_address == user.email_address:
            return forms.ValidationError('Yo')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email_address']

        if commit: 
            user.save()

        return user


class LogInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password',)

