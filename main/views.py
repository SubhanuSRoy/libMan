from django.shortcuts import render,redirect
from . models import *

from . forms import BookForm
# Create your views here.
def home(request):
    return render(request,'main/home.html')

def books(request):
    books = Book.objects.all()
    context={'books':books}
    return render(request,'main/books.html',context)

# func to create book
def createBook(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}
    return render(request,'main/book_form.html',context)

# func to update details/copies of books
def updateBook(request,pk):
    # get the specific book by its id
    book = Book.objects.get(id=pk)
    # pass the already filled fields to this form
    form = BookForm(instance=book)

    # get the form data and if valid then save and redirect to home page
    if request.method == 'POST':
        # this time also pass the instance of the book with changes
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books')
   

    context={'form':form}   
    return render(request,'main/book_form.html',context)

def deleteBook(request,pk):
    book = Book.objects.get(id=pk)

    if request.method == 'POST':
        book.delete()
        return redirect('books')
    context = {'book':book,'bookName':book.title}
    return render(request,'main/delete.html',context)