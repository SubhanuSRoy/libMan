from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('books/',views.books,name='books'),
    # path('register/',views.registerPage,name='register'),
    # path('login/',views.loginPage,name='login'),
    # path('logout/',views.logoutUser,name='logout'),
    # path('userPage/',views.userPage,name='userPage'),
    # path('products/',views.products,name='products'),
    # path('customer/<str:pk>',views.customer,name='customer'),

    path('create_book',views.createBook,name='create_book'),
    path('update_book/<str:pk>',views.updateBook,name='update_book'),
    path('delete_book/<str:pk>',views.deleteBook,name='delete_book')
]