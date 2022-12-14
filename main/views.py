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

# for search func of books
from . filters import BookFilter

# decorators to restricyt permissions of user
from . decorators import admin_only,allowed_users,unauthenticated_user


from django.http import JsonResponse
from . serializers import CustomerSerializer
# Create your views here.

@unauthenticated_user
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

@unauthenticated_user
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

@admin_only
def home(request):
    books_count=Book.objects.all().count()
    issues_count=Issue.objects.all().count()
    customers=Customer.objects.all()
    context={'books_count':books_count,'issues_count':issues_count,'customers':customers}
    return render(request,'main/home.html',context)

def books(request):
    books = Book.objects.all()

    # when user changes filters, the query changes
    bookfilter = BookFilter(request.GET,queryset=books)

    # update the orders shown to be as per the queryset of the orderFilter which user wants
    books=bookfilter.qs
    context={'books':books,'filter':bookfilter}
    return render(request,'main/books.html',context)

@admin_only
def customer(request,pk):
    # here pk is the id of the customer
    customer = Customer.objects.get(id=pk)
    issues = customer.issue_set.all()
    context={'issues':issues, 'cust':customer}
    return render(request,'main/customer.html',context)

@admin_only
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

@admin_only
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

@allowed_users(allowed_roles=['customer'])
def userPage(request):
    # all issues of the specific logged in user
    issues = request.user.customer.issue_set.all()
    total_issues = issues.count()
    custName=request.user.customer.name
    context={'issues':issues,'custName':custName}
    return render(request,'main/user_home.html',context)

@allowed_users(allowed_roles=['customer'])
# func to issue book
def issueBook(request,pk):
    issue_book = Book.objects.get(id=pk)
    issue_customer=request.user.customer
    issues = request.user.customer.issue_set.all()
    # traverse through all the issues and add the book titles to addBook dict
    allBooks={} #stores the names of the issued books of the current user
    for issue in issues:
        allBooks[issue.book.title]=1

    # now check if requested book's title matches with any of the books in allBooks
    # if yes that means it has already been issued
    if issue_book.title in allBooks:
        messages.success(request,issue_book.title + ' has already been issued to you ')
        return redirect('userPage')
    else:
        # reduce copies of the book
        issue_book.copies -= 1
        # save the updated value
        issue_book.save()
        
        Issue.objects.create(customer=issue_customer,book=issue_book)
        # show flash message
        messages.success(request,issue_book.title + ' has been issued to '+ issue_customer.name)
        return redirect('userPage')
    
@allowed_users(allowed_roles=['customer'])
# func to return book
def returnBook(request,pk):
    # here pk is the id of the issue
    return_issue = Issue.objects.get(id=pk)
    # get the book which is linked to that issue
    return_book = return_issue.book

    return_customer=request.user.customer
   
    # now increase copies of the book
    return_book.copies += 1
    # save the updated value
    return_book.save()
    # delete that issue from the db
    return_issue.delete()
    # show flash message
    messages.warning(request,return_book.title + ' has been returned by '+ return_customer.name)
    return redirect('userPage')

def customer_list(request):
    customers = Customer.objects.all()
    custSerializer=CustomerSerializer(customers,many=True)
    return JsonResponse({'customers':custSerializer.data},safe=False)
