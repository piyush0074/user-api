'''from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	
	class Meta:
		model = CustomUser
		field = ('username','first_name','last_name','email')'''