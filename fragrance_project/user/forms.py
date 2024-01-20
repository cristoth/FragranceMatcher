from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
# from phonenumber_field.formfields import PhoneNumberField


# class for a form extending UserCreationForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # default: required = true
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:  # nested namespace for configurations: the model with which this class interacts
        model = User  # creating a new User, when form validates
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']  # pass1 - actual pass, pass2 - confirmation pass


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()  

    class Meta:  
        model = User  
        fields = ['first_name', 'last_name', 'username', 'email']  # update only username & email


class MyDateInput(forms.widgets.DateInput):
    input_type = 'date'


class ProfileUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(widget=MyDateInput())

    class Meta:
        model = Profile
        fields = ['image', 'birthdate']


