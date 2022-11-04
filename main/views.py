from django.shortcuts import render,redirect
from . models import *

from . forms import BookForm

# made a custom form to add more details when creating user
from . forms import CustomCreateUserForm

# flash message
from django.contrib import messages

#for auth,login,logout functionality of users
from django.contrib.auth import authenticate,login,logout

# to add the customer group to each new user created
from django.contrib.auth.models import Group

# Create your views here.

def registerPage (request):
    form = CustomCreateUserForm()
    if request.method == 'POST':
        form = CustomCreateUserForm(request.POST)
        if form.is_valid():
            # get the user which was created
            user=form.save( )
            # now add that user to the customer group
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            # get the username of the new user so we can show in message
            username = form.cleaned_data.get('username')

            Customer.objects.create(user=user,name=user.username,email=user.email)
            # show flash message
            messages.success(request,'Account was created for '+ username)

            return redirect ('login')
    context={'form':form}
    return render(request,'main/register.html',context)


def loginPage (request):

    if request.method=='POST':
        name = request.POST.get('username')
        passw = request.POST.get('password')
        # authenticate the user now
        user = authenticate(request,username=name,password=passw)
        # now check if user exists only then proceed
        if user is not None:
            login(request,user )
            return redirect('home')
        else:
            messages.info(request,'Username or Password incorrect')
            # if incorrect then it will take them to the login page again
    return render(request,'main/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


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

# function to delete a book from db
# def deleteBook(request,pk):
#     book = Book.objects.get(id=pk)

#     if request.method == 'POST':
#         book.delete()
#         return redirect('books')
#     context = {'book':book,'bookName':book.title}
#     return render(request,'main/delete.html',context)

