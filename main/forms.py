from django.forms import ModelForm
from . models import Book

class BookForm(ModelForm):
    class Meta:
        # you need a form for which model
        model= Book
        # when you want to create a form with all the fields
        fields= '__all__'