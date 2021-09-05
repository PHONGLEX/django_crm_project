from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Order, Customer


class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = "__all__"


class CreateUserForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={
		"class": "form-control",
		"type": "text"
		}))
	email = forms.CharField(widget=forms.TextInput(attrs={
		"class": "form-control",
		"type": "email"
		}))
	password1 = forms.CharField(widget=forms.TextInput(attrs={
		"class": "form-control",
		"type": "password"
		}))
	password2 = forms.CharField(widget=forms.TextInput(attrs={
		"class": "form-control",
		"type": "password"
		}))
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")


class LoginUserForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={
		"class": "form-control",
		"type": "text"
		}))
	password = forms.CharField(widget=forms.TextInput(attrs={
		"class": "form-control",
		"type": "password"
		}))
	class Meta:
		model = User
		fields = ("username", "password")


class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = "__all__"
		exclude = ("user",)