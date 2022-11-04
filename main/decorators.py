from django.http import HttpResponse
from django.shortcuts import redirect

# this is to redirect authenticated users to home page. they cant access login and register pages when logged in already
# it checks if a user is not authenticated then it will return to home page
def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
       
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)

    return wrapper_func

# decorator to mention which roles can access a certain page
# here in our case, we have added some users to customer group and some to admin group
# if they are part of admin group then they can access all pages
# else when they try to access other pages then they get the HTTPReponse message
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group=None

            # we get the name of the user's group
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            # if its in the allowed roles mentioned then we show them the page else she show HTTPResponse
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('You are not authorized to view')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group=None
        # get the current user's group name
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        

        # if group is admin then show them the page
        if group == 'admin':
            return view_func(request,*args,**kwargs)
        # if group is customer then show the user page
        else:
            return redirect('userPage')
    return wrapper_func

