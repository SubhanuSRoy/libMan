from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('books/',views.books,name='books'),
    path('register/',views.registerPage,name='register'),
    path('',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('userPage/',views.userPage,name='userPage'),
    path('customer/<str:pk>',views.customer,name='customer'),
    path('issue_book/<str:pk>',views.issueBook,name='issue_book'),
    path('return_book/<str:pk>',views.returnBook,name='return_book'),

    path('create_book',views.createBook,name='create_book'),
    path('update_book/<str:pk>',views.updateBook,name='update_book'),
    # path('delete_book/<str:pk>',views.deleteBook,name='delete_book')

    path('api/customer_list',views.customer_list)
]