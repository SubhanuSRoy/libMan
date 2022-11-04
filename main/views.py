from django.shortcuts import render
from . models import *
# Create your views here.
def home(request):
    return render(request,'main/home.html')

def books(request):
    books = Book.objects.all()
    context={'books':books}
    return render(request,'main/books.html',context)