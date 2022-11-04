from django.forms import ModelForm
from . models import Book

# we want to make a user registration form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class BookForm(ModelForm):
    class Meta:
        # you need a form for which model
        model= Book
        # when you want to create a form with all the fields
        fields= '__all__'

class CustomCreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']